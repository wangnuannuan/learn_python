from __future__ import print_function, absolute_import, unicode_literals
from embarc_tools.utils import merge_recursive, uniqify, pquery
from embarc_tools.exporter import Exporter
from embarc_tools.osp import osp
import os
import random
from embarc_tools.settings import *
from embarc_tools.notify import TerminalNotifier
import collections
from embarc_tools.download_manager import cd
class Generator:

    def generate(self, name=""):

        yield Ide()

class Ide:
    def __init__(self, path=None):
        #self.name = name
        self.ide = {}
        self.ide["common"] = {}
        self.ide["common"] = self._get_project_file_template()
        self.notifier = TerminalNotifier()
        if path:
            self.ide["common"]["path"] = path
        else:
            self.ide["common"]["path"] = os.getcwd().replace("\\", "/")
        self.notifier.event["format"] = "string"
        self.notifier.event["type"] = "info"
        self.notifier.event["message"] = "Start to generate IDE project "
        self.notifier.notify(self.notifier.event)
    def _get_project_file_template(self, name="Default"):
        project_template = {
            "name": name,
            "path":"",
            "folder": "",
            "root": "",
            "outdir": "${ProjDirPath}",
        }
        return project_template

    def _get_cproject_template(self):

        cproject_template = {
            "core": {}, #//duqu
            "includes": [],
            "defines": [],
            "build": "",
            "clean": "",
            "toolchain": "",
        }
        return cproject_template

    def _get_build_template(self):

        build_template = {
            "APPL": "",
            "BOARD": "",
            "BD_VER": "",
            "CUR_CORE": "",
            "TOOLCHAIN": "",
        }

        return build_template

    def _get_project_conf_template(self):
        cproject_template = self._get_cproject_template()
        build_template = self._get_build_template()

        osppath = osp.OSP()
        makefile, current_build_template = osppath.get_makefile_config(build_template, verbose=True)
        build_template = collections.OrderedDict()
        osp_root, update = osppath.check_osp(current_build_template["EMBARC_OSP_ROOT"])
        if update:
            osppath.update_makefile(osp_root, os.getcwd())
        current_build_template["EMBARC_OSP_ROOT"] = osp_root
        self.ide["common"]["root"] = osp_root
        self.ide["common"]["folder"] = os.path.relpath(os.getcwd(), osp_root).replace("\\", "/").strip("../")

        make_tool = "make"
        if current_build_template.get("TOOLCHAIN") == "mw":
            make_tool = "gmake"
        opt_command = [make_tool]
        opt_command.append("opt")
        cmd_output = pquery(opt_command)

        includes = list()
        compile_opts = ""
        relative_root = ""
        if cmd_output:
            opt_lines = cmd_output.splitlines()
            for opt_line in opt_lines:
                if opt_line.startswith("APPL"):
                    current_build_template["APPL"] = (opt_line.split(":", 1)[1]).strip()
                build_template["APPL"] = current_build_template.get("APPL")
                if opt_line.startswith("BOARD"):
                    current_build_template["BOARD"] = (opt_line.split(":", 1)[1]).strip()
                build_template["BOARD"] = current_build_template.get("BOARD")
                if opt_line.startswith("BD_VER"):
                    current_build_template["BD_VER"] = (opt_line.split(":", 1)[1]).strip()
                build_template["BD_VER"] = current_build_template.get("BD_VER")
                if opt_line.startswith("CUR_CORE"):
                    current_build_template["CUR_CORE"] = (opt_line.split(":", 1)[1]).strip()
                build_template["CUR_CORE"] = current_build_template.get("CUR_CORE")
                if opt_line.startswith("TOOLCHAIN"):
                    current_build_template["TOOLCHAIN"] = (opt_line.split(":", 1)[1]).strip()
                build_template["TOOLCHAIN"] = current_build_template.get("TOOLCHAIN")
                if opt_line.startswith("EMBARC_ROOT"):
                    relative_root = (opt_line.split(":", 1)[1]).strip()
                    osp_root = os.path.normpath(os.path.join(os.getcwd(), relative_root))
                    self.ide["common"]["root"] = osp_root.replace("\\", "/")
                    self.ide['common']['osp_root'] = os.path.basename(osp_root)
                    current_build_template["EMBARC_OSP_ROOT"] = osp_root
                build_template["EMBARC_OSP_ROOT"] = current_build_template.get("EMBARC_OSP_ROOT")
                if  opt_line.startswith("COMPILE_OPT") == True:
                    compile_opt_line = opt_line.split(":", 1)[1]
                    compile_opts = compile_opt_line.split()
        self.notifier.event["message"] = "Get inculdes and defines "
        self.notifier.notify(self.notifier.event)
        if compile_opts != "" and relative_root != "":
            for comp_opt in compile_opts:
                if comp_opt.startswith("-I") == True:
                    inc_path = comp_opt.replace("-I", "", 1)
                    if inc_path.startswith(relative_root):
                        inc_path = os.path.relpath(inc_path, relative_root)
                    inc_path = inc_path.replace("\\","/")

                    includes.append(inc_path)
                if comp_opt.startswith("-D") == True:
                    define = comp_opt.replace("-D", "", 1)

                    define = define.replace('\\"', '&quot;')
                    define = define.replace('"', '&quot;')

                    cproject_template["defines"].append(define)

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
        build_template["OUT_DIR_ROOT"] = "${ProjDirPath}"

        cur_core = build_template["CUR_CORE"]
        self.ide["common"]["name"] = build_template["APPL"]

        for core, settings in CORES.items():
            if cur_core == core:
                cproject_template["core"] = {core: settings}

        for core, settings in cproject_template["core"].items():
            core_id = random.randint(1000000000, 2000000000)
            cproject_template["core"][core]["id"] = core_id

        for path in includes:
            include = os.path.join(self.ide['common']["name"], "embARC", path)

            if path == ".":
                include = self.ide["common"]["name"]

            include = include.replace("\\", "/")
            cproject_template["includes"].append(include)


        self.ide["toolchain"] = build_template["TOOLCHAIN"]
        self.ide["common"]["links_folder"] = list()
        self.ide["common"]["links_file"] = list()

        link_folders, link_files, virtual_folders = self.set_link_folders(includes, current_build_template)

        self.ide["common"]["links_folder"].extend(link_folders)
        self.ide["common"]["links_file"].extend(link_files)

        self.ide["common"]["virtual_folders"] = uniqify(virtual_folders)

        return cproject_template

    def set_link_folders(self, includes, makefile_config=None):
        link_folders = list()
        for path in includes:
            if path != "." and "embARC_generated" not in path:
                if "/" in path:
                    if path.startswith("board"):
                        link_folders.append(path.rsplit("/", 2)[0])
                    else:
                        link_folders.append(path)

        link_folders = uniqify(link_folders)

        need_pop = list()
        for i in range(len(link_folders)):
            link = link_folders[i]
            for path in link_folders:
                if path != link and path.startswith(link):
                    need_pop.append(path)
        for path in link_folders:
            if path.startswith("inc"):
                need_pop.append(path)
            if path.startswith("options"):
                need_pop.append(path)
            if path.startswith("arc"):
                need_pop.append(path)

        for pop_path in need_pop:
            if pop_path in link_folders:
                link_folders.remove(pop_path)

        link_folders.append("inc")
        link_folders.append("options")
        link_folders.append("arc")
        link_folders.append("device\\ip")
        link_folders.append("device\\inc")
        if makefile_config:
            os_sel = makefile_config.get("os", None)
            lib_sel = makefile_config.get("lib", None)
            if os_sel:
                link_folders.append("os/" + os_Sel)
            if lib_sel:
                link_folders.append("library/" + lib_Sel)
        virtual_folders = list()
        for link in link_folders:
            if "/" in link:
                link_depth = len(link.split("/"))
                link_list = [link.rsplit("/", i)[0] for i in range(link_depth, 0, -1)]
                virtual_folders.extend(link_list)
        link_files = list()
        osp_root = self.ide["common"]["root"]
        for folder in virtual_folders:
            folder_path = os.path.join(osp_root, folder)
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    relative_path = os.path.join(folder, file).replace("\\", "/")
                    link_files.append(relative_path)
        current_virtual_folders = list()
        for link in link_folders:
            link = "embARC/" + link
            if "/" in link:
                link_depth = len(link.split("/"))
                link_list = [link.rsplit("/", i)[0] for i in range(link_depth, 0, -1)]
                current_virtual_folders.extend(link_list)
        return link_folders, link_files, current_virtual_folders


    @staticmethod
    def _list_elim_none(list_to_clean):
        return [l for l in list_to_clean if l]

    @staticmethod
    def _dict_elim_none(dic_to_clean):
        dic = dic_to_clean
        try:
            for k, v in dic_to_clean.items():
                if type(v) is list:
                    dic[k] = Ide._list_elim_none(v)
                elif type(v) is dict:
                    dic[k] = Ide._dict_elim_none(v)
        except AttributeError:
            pass
        return dic

    def _set_project_attributes(self, key_values, destination, source): # source --> destination
        if key_values in source:
            for attribute, data in source[key_values].items():
                if attribute in destination:

                    if type(destination[attribute]) is list:
                        if type(data) is list:
                            destination[attribute].extend(data)
                        else:
                            destination[attribute].append(data)
                    elif type(destination[attribute]) is dict:
                        destination[attribute] = Ide._dict_elim_none(merge_recursive(destination[attribute], data))
                    else:
                        if type(data) is list:
                            if data[0]:
                                destination[attribute] = data[0]
                        else:
                            if data:
                                destination[attribute] = data[0]
    def get_asm_c_include(self):
        self.ide["exporter"] = self._get_project_conf_template()
        self.ide["exporter"].update(self.ide["common"])

    def generate(self):
        with cd(self.ide["common"]["path"]):

            self.get_asm_c_include()
            outdir = "."
            if "path" in self.ide["common"]:
                app_path = self.ide["common"]["folder"]
                path_depth = len(app_path.split("/"))

            exporter = Exporter(self.ide["toolchain"])
            self.notifier.event["format"] = "string"
            self.notifier.event["message"] = "Start to generate IDE project accroding to templates (.project.tmpl and .cproject.tmpl)"
            self.notifier.notify(self.notifier.event)
            exporter.gen_file_jinja("project.tmpl", self.ide["common"], ".project", outdir)
            exporter.gen_file_jinja(".cproject.tmpl", self.ide["exporter"], ".cproject", outdir)
            self.notifier.event["message"] = "Finish generate IDE project and the files are in " + os.path.abspath(outdir)
            self.notifier.notify(self.notifier.event)
            self.notifier.event["message"] = "Open ARC GNU IDE (version) Eclipse - >File >Open Projects from File System >Paste " + os.path.abspath(outdir)
            self.notifier.notify(self.notifier.event)
