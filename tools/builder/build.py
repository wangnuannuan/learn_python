from __future__ import print_function, absolute_import
import sys
import os
import subprocess
import time
from tools.settings import *
from .. download_manager import mkdir, delete_dir_files
from tools.notify import TerminalNotifier
from tools.osp import osp
BUILD_OPTION_NAMES=['BOARD', 'BD_VER', 'CUR_CORE', 'TOOLCHAIN', 'OLEVEL', 'V', 'DEBUG', 'SILENT', 'JTAG']
BUILD_INFO_NAMES=['EMBARC_ROOT', 'OUT_DIR_ROOT', 'BUILD_OPTION', 'APPLICATION_NAME', 'APPLICATION_LINKSCRIPT', 'APPLICATION_ELF', 'APPLICATION_BIN', 'APPLICATION_HEX', 'APPLICATION_MAP', 'APPLICATION_DUMP', 'APPLICATION_DASM', 'MIDDLEWARE', 'PERIPHERAL']
BUILD_CFG_NAMES=['EMBARC_ROOT', 'OUT_DIR_ROOT', 'COMPILE_OPT', 'CXX_COMPILE_OPT', 'ASM_OPT', 'AR_OPT', 'LINK_OPT', 'DEBUGGER', 'DBG_HW_FLAGS', 'MDB_NSIM_OPT']
BUILD_SIZE_SECTION_NAMES=['text', 'data', 'bss']

class embARC_Builder:
    def __init__(self, osproot=None, buildopts=None, outdir=None):
        self.buildopts = dict()
        self.notifier = TerminalNotifier()

        make_options = ' '
        if osproot is not None and os.path.isdir(osproot):
            self.osproot = os.path.realpath(osproot)
            self.buildopts["EMBARC_ROOT"] = self.osproot
            make_options += 'EMBARC_ROOT=' + str(self.osproot) + ' '
        else:
            self.osproot = None
        if outdir is not None:
            self.outdir = os.path.realpath(outdir)
            make_options += 'OUT_DIR_ROOT=' + str(self.outdir) + ' '
        else:
            self.outdir = None

        if buildopts is not None:
            for opt in BUILD_OPTION_NAMES:
                if opt in buildopts:
                    self.buildopts[opt] = str(buildopts[opt]).strip()
                    option = str(opt) + '=' + self.buildopts[opt] + ' '
                    make_options += option
        self.make_options = make_options

        pass

    @staticmethod
    def build_common_check(app):
        build_status = {'result': True, 'reason':''}
        app_normpath = os.path.normpath(app)
        if os.path.isdir(app_normpath) == False:
            build_status['reason'] = 'Application folder doesn\'t exist!'
            build_status['result'] = False
        if not (os.path.exists(app_normpath+'/makefile') or \
                os.path.exists(app_normpath+'/Makefile') or \
                os.path.exists(app_normpath+'/GNUmakefile')):
            build_status['reason'] = 'Application makefile donesn\'t exist!'
            build_status['result'] = False

        app_realpath=os.path.realpath(app_normpath)
        build_status['app_path'] = app_realpath

        return app_realpath, build_status

    def _config_coverity(self, app):
        print("config coverity")
        app_normpath = os.path.normpath(app)
        app_realpath=os.path.realpath(app_normpath)

        build_status = {'result': True, 'reason':''}
        self.coverity_data = os.path.join(app, "coverity_data")
        self.coverity_config = os.path.join(self.coverity_data, "coverity-config.xml")
        self.coverity_html = os.path.join(app, "coverity_html")
        if os.path.exists(self.coverity_data):
            delete_dir_files(self.coverity_data)
            mkdir(self.coverity_data)
        if os.path.exists(self.coverity_html):
            delete_dir_files(self.coverity_html)
        if 'gnu' in self.make_options:
            self.coverity_comptype = 'gcc'
            self.coverity_compiler = 'arc-elf32-gcc'
        elif 'mw' in self.make_options:
            self.coverity_comptype = 'clangcc'
            self.coverity_compiler = 'ccac'
        else:
            build_status['reason'] = 'Toolchian is not supported!'
            build_status['result'] = False
        if build_status['result']:
            print("BEGIN SECTION Configure Coverity to use the built-incompiler")
            config_compilercmd = "cov-configure --config " + self.coverity_config + " --template --comptype "+ self.coverity_comptype +" --compiler " + self.coverity_compiler
            subprocess.Popen(config_compilercmd, shell=True, cwd=str(app_realpath),stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return build_status

    def build_target(self, app, target=None, parallel=False, coverity=False):
        app_realpath, build_status = self.build_common_check(app)
        build_status['build_target'] = target
        build_status['time_cost'] = 0
        self.notifier.event["message"] = "build target: %s " % target
        self.notifier.notify(self.notifier.event)


        if build_status['result'] == False:
            return build_status

        ### Check and create output directory
        if self.outdir is not None and os.path.isdir(self.outdir) == False:
            print("Create application output directory: " + self.outdir)
            os.makedirs(self.outdir)

        build_precmd = "make "
        if parallel:
            build_precmd += '-j '
        build_precmd += self.make_options

        if type(target) is str or target is None:
            build_cmd = build_precmd + " " + str(target)
        else:
            build_status['reason'] = "Unrecognized build target"
            build_status['result'] = False
            return build_status

        if coverity:
            print("build application with coverity")
            build_status = self._config_coverity(app)
            if build_status['result'] == False:
                return build_status
            coverity_build_precmd = "cov-build --config " + self.coverity_config + " --dir " + self.coverity_data
            build_cmd = coverity_build_precmd + " " + build_cmd

        self.notifier.event["message"] = "build command: %s " % build_cmd
        self.notifier.notify(self.notifier.event)

        time_pre = time.time()
        build_status['build_cmd'] = build_cmd
        build_status['build_msg'] = ''

        build_config = None
        if target != "info":
            build_config_template = self.get_build_template()
            build_config = self.get_makefile_config(build_config_template)

            build_cmd_list = build_cmd.split()

            for i in range(len(build_cmd_list)):
                if build_cmd_list[i].startswith("EMBARC_ROOT"):
                    build_cmd_list[i] = "EMBARC_ROOT=" + self.osproot
            build_cmd = " ".join(build_cmd_list)


        self.notifier.event["message"] = "start to build application"
        self.notifier.notify(self.notifier.event)

        build_proc = subprocess.Popen(build_cmd, shell=True, cwd=str(app_realpath), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
        if target not in ["size"]:
            for line in iter(build_proc.stdout.readline, b''):
                    print(line, end='')
        try:
            (build_out, build_err) = build_proc.communicate()
            return_code = build_proc.poll()
            build_status['build_msg'] = build_out
        except OSError as e:
            print("Run command({}) failed!".format(build_command))
            build_status['build_msg'] = "Build target command failed"
            build_status['time_cost'] = (time.time() - time_pre)
            build_status['result'] = False
            del build_proc
            return build_status
        del build_proc

        build_status['time_cost'] = (time.time() - time_pre)
        self.notifier.event["message"] = "Completed in: (%s)s  " % build_status['time_cost']
        self.notifier.notify(self.notifier.event)

        build_result = "build successfully"
        if return_code != 0:
            build_status['result'] = False
        if not build_status['result']:
            build_result = "build failed "
            build_result = build_result + build_status.get('reason', "")

        self.notifier.event["message"] = build_result
        self.notifier.notify(self.notifier.event)
        return build_status

    def build_coverity_result(self):
        app = os.path.dirname(self.coverity_data)
        app_normpath = os.path.normpath(app)
        app_realpath=os.path.realpath(app_normpath)
        print("BEGIN SECTION Coverity Analyze Defects")
        coverity_analyzecmd = "cov-analyze --dir " + self.coverity_data
        subprocess.Popen(coverity_analyzecmd, shell=True, cwd=str(app_realpath),stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print("BEGIN SECTION Coverity Format Errors into HTML")
        coverity_errorcmd = "cov-format-errors --dir " + self.coverity_data + " -x -X --html-output "+ self.coverity_html
        subprocess.Popen(coverity_errorcmd, shell=True, cwd=str(app_realpath),stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def upload_coverity(self, app, server=None, user=None, password=None):
        app_normpath = os.path.normpath(app)
        app_realpath=os.path.realpath(app_normpath)
        app_name = copy.deepcopy(app).replace("/", "_")
        print("BEGIN SECTION Coverity Commit defects to {}".format(server))
        upload_coveritycmd = "cov-commit-defects --dir " + self.coverity_data + " --host "+ server + " --user " + user + " --password " + password
        subprocess.Popen(upload_coveritycmd, shell=True, cwd=str(app_realpath),stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def get_build_info(self, app):
        build_status = self.build_target(app, target='opt')
        if build_status['result'] == False:
            return build_status

        build_out = build_status['build_msg']
        build_cfg = dict()
        cfg_lines = build_out.splitlines()

        for cfg_line in cfg_lines:
            words = cfg_line.split(':')
            if len(words) == 2:
                key = words[0].strip()
                value = words[1].strip()
                if key in BUILD_CFG_NAMES or key in BUILD_OPTION_NAMES:
                    build_cfg[key] = value

        build_status['build_cfg'] = build_cfg

        ### Get Build Info
        info_status = self.build_target(app, target='info')
        build_out = info_status['build_msg']
        build_info = dict()
        if info_status['result']:
            info_lines = build_out.splitlines()
            for info_line in info_lines:
                words = info_line.split(':')
                if len(words) == 2:
                    key = words[0].strip()
                    value = words[1].strip()
                    if key in BUILD_INFO_NAMES:
                        build_info[key] = value
                    if key == 'BUILD_OPTION':
                       build_cfgs_dict = value.split()
                       for cfg_dict in build_cfgs_dict:
                           cfg_pair = cfg_dict.split('=')
                           if len(cfg_pair) == 2 and cfg_pair[0] in BUILD_OPTION_NAMES:
                               build_status['build_cfg'][cfg_pair[0]] = cfg_pair[1]
                    if key == 'MIDDLEWARE' or key == 'PERIPHERAL':
                        build_info[key+'S'] = value.split()
                    if key == 'APPLICATION_ELF':
                        build_info['APPLICATION_OUTDIR'] = os.path.dirname(value)
        build_status['build_info'] = build_info

        app_realpath = build_status['app_path']
        if 'EMBARC_ROOT' in build_status['build_cfg']:
            if not os.path.isabs((build_status['build_cfg']['EMBARC_ROOT'])):
                build_status['build_cfg']['EMBARC_ROOT'] = os.path.realpath(os.path.join(app_realpath, build_status['build_cfg']['EMBARC_ROOT']))
        if 'OUT_DIR_ROOT' in build_status['build_cfg']:
            if not os.path.isabs(build_status['build_cfg']['OUT_DIR_ROOT']):
                build_status['build_cfg']['OUT_DIR_ROOT'] = os.path.realpath(os.path.join(app_realpath, build_status['build_cfg']['OUT_DIR_ROOT']))
        if 'OUT_DIR_ROOT' in build_status['build_info']:
            if not os.path.isabs(build_status['build_info']['OUT_DIR_ROOT']):
                build_status['build_info']['OUT_DIR_ROOT'] = os.path.realpath(os.path.join(app_realpath, build_status['build_info']['OUT_DIR_ROOT']))
        if 'APPLICATION_ELF' in build_status['build_info']:
            if not os.path.isabs(build_status['build_info']['APPLICATION_ELF']):
                build_status['app_elf'] = os.path.realpath(os.path.join(app_realpath, build_status['build_info']['APPLICATION_ELF']))
            else:
                build_status['app_elf'] = build_status['build_info']['APPLICATION_ELF']
        if 'APPLICATION_HEX' in build_status['build_info']:
            if not os.path.isabs(build_status['build_info']['APPLICATION_HEX']):
                build_status['app_hex'] = os.path.realpath(os.path.join(app_realpath, build_status['build_info']['APPLICATION_HEX']))
            else:
                build_status['app_hex'] = build_status['build_info']['APPLICATION_HEX']
        if 'APPLICATION_BIN' in build_status['build_info']:
            if not os.path.isabs(build_status['build_info']['APPLICATION_BIN']):
                build_status['app_bin'] = os.path.realpath(os.path.join(app_realpath, build_status['build_info']['APPLICATION_BIN']))
            else:
                build_status['app_bin'] = build_status['build_info']['APPLICATION_BIN']
        if 'APPLICATION_OUTDIR' in build_status['build_info']:
            if not os.path.isabs(build_status['build_info']['APPLICATION_OUTDIR']):
                build_status['app_outdir'] = os.path.realpath(os.path.join(app_realpath, build_status['build_info']['APPLICATION_OUTDIR']))
            else:
                build_status['app_outdir'] = build_status['build_info']['APPLICATION_OUTDIR']

        return build_status

    def build_elf(self, app, parallel=False, pre_clean=False, post_clean=False):
        ### Clean Application before build if requested
        if pre_clean:
            build_status = self.build_target(app, parallel=parallel, target='clean')
            if build_status['result'] == False:
                return build_status

        ### Build Application
        build_status = self.build_target(app, parallel=parallel, target='all')
        if build_status['result'] == False:
            return build_status
        ### Clean Application after build if requested
        if post_clean:
            clean_status = self.build_target(app, parallel=parallel, target='clean')
            if clean_status['result'] == False:
                return clean_status

        return build_status

    def build_bin(self, app, parallel=False, pre_clean=False, post_clean=False):
        ### Clean Application before build if requested
        if pre_clean:
            build_status = self.build_target(app, parallel=parallel, target='clean')
            if build_status['result'] == False:
                return build_status

        ### Build Application
        build_status = self.build_target(app, parallel=parallel, target='bin')
        if build_status['result'] == False:
            return build_status
        ### Clean Application after build if requested
        if post_clean:
            clean_status = self.build_target(app, parallel=parallel, target='clean')
            if clean_status['result'] == False:
                return clean_status

        return build_status

    def build_hex(self, app, parallel=False, pre_clean=False, post_clean=False):
        ### Clean Application before build if requested
        if pre_clean:
            build_status = self.build_target(app, parallel=parallel, target='clean')
            if build_status['result'] == False:
                return build_status

        ### Build Application
        build_status = self.build_target(app, parallel=parallel, target='hex')
        if build_status['result'] == False:
            return build_status
        ### Clean Application after build if requested
        if post_clean:
            clean_status = self.build_target(app, parallel=parallel, target='clean')
            if clean_status['result'] == False:
                return clean_status

        return build_status

    def get_build_size(self, app):
        build_status = self.build_target(app, target='size')
        build_size = dict()
        if build_status['result'] == True:
            app_size_lines = build_status['build_msg'].splitlines()
            if len(app_size_lines) >= 3:
                app_size_lines = app_size_lines[len(app_size_lines)-2:]
                section_names = app_size_lines[0].split()
                section_values = app_size_lines[1].split()
                for idx, section_name in enumerate(section_names):
                    if section_name in BUILD_SIZE_SECTION_NAMES:
                        build_size[section_name] = int(section_values[idx])
            else:
                build_status['result'] = False
        self.notifier.event["format"] = "table"
        table_head = ["", "application Program Size"]
        table_content = list()

        for key, value in build_size.items():
            table_content.append([key, value])
        self.notifier.event["message"] = [table_head, table_content]
        self.notifier.notify(self.notifier.event)
        build_status['build_size'] = build_size


        return build_status

    def clean(self, app):
        build_status = self.build_target(app, target='clean')
        return build_status

    def distclean(self, app):
        build_status = self.build_target(app, target='distclean')
        return build_status

    def boardclean(self, app):
        build_status = self.build_target(app, target='boardclean')
        return build_status

    def get_makefile_config(self, build_template=None):
        makefile = None
        for file in MakefileNames:
            if os.path.exists(file) and os.path.isfile(file):
                makefile = file

        if not makefile:
            return None
        with open(makefile) as f:
            lines = f.read().splitlines()
            for line in lines:
                if line.startswith("APPL "):
                    build_template["APPL"] = (line.split("=")[1]).strip()
                if line.startswith("BOARD"):
                    build_template["BOARD"] = (line.split("=")[1]).strip()
                if line.startswith("BD_VER"):
                    build_template["BD_VER"] = (line.split("=")[1]).strip()
                if line.startswith("CUR_CORE"):
                    build_template["CUR_CORE"] = (line.split("=")[1]).strip()
                if line.startswith("TOOLCHAIN"):
                    build_template["TOOLCHAIN"] = (line.split("=")[1]).strip()
                    if build_template["TOOLCHAIN"] and build_template["TOOLCHAIN"] != "":
                        pass
                    else:
                        build_template["TOOLCHAIN"] = "gnu"
                if line.startswith("EMBARC_ROOT"):
                    build_template["EMBARC_ROOT"] = (line.split("=")[1]).strip()
        for key , value in self.buildopts.items():
            if key in build_template:
                build_template[key] = value
        self.notifier.event["message"] = "Current configuration "
        self.notifier.notify(self.notifier.event)
        self.notifier.event["format"] = "table"
        table_head = list()
        table_content = list()
        for key, value in build_template.items():
            table_head.append(key)
            table_content.append(value)
        self.notifier.event["message"] = [table_head, [table_content]]
        self.notifier.notify(self.notifier.event)
        osppath = osp.OSP()
        osp_root = build_template["EMBARC_ROOT"]
        if not osppath.is_osp(osp_root):
            self.notifier.event["type"] = "warning"
            self.notifier.event["message"] = "current EMBARC_ROOT is not a valid osp root"
            self.notifier.notify(self.notifier.event)
            osppath.list_path()
            while True:
                input_root = raw_input("choose osp root or set another path as osp root: ")
                osp_root = osppath.is_osp(input_root)

                if not osp_root:
                    self.notifier.event["format"] = "string"
                    self.notifier.event["type"] = "warning"
                    self.notifier.event["message"] = "what you choose is not a valid osp root"
                    self.notifier.notify(self.notifier.event)
                    osp_root = osppath.get_path()
                    if osp_root:
                        self.notifier.event["message"] = "here choose " + osp_root + " as osp root"
                        self.notifier.notify(self.notifier.event)
                        break
                    else:
                        osppath.clear_path()
                        self.notifier.event["type"] = "default"
                        self.notifier.event["message"] = "please set a valid osp root or download embarc osp first"
                        self.notifier.notify(self.notifier.event)
                        continue

                break
            self.osproot = osp_root
            osppath.set_path(osp_root)

        return build_template

    def get_build_template(self):
        build_template = {
            "BOARD": "",
            "BD_VER": "",
            "CUR_CORE": "",
            "TOOLCHAIN": "",
            "APPL": "",


        }
        return build_template
