from tools.utils import merge_recursive, uniqify, pquery
from tools.exporter import Exporter
import os
import random
from tools.settings import *
import logging
from tools.notify import TerminalNotifier

logger = logging.getLogger("ide.project")

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
        os.chdir(self.ide["common"]["path"])
        self.notifier.event["format"] = "string"
        self.notifier.event["type"] = "info"
        self.notifier.event["message"] = "Start to generate ide "
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
            "BOARD": "",
            "BD_VER": "",
            "CUR_CORE": "",
            "TOOLCHAIN": "",
            "APPL": "",
            

        }
        return build_template

    def _get_makefile_config(self, build_template=None):
        self.notifier.event["message"] = "Read makefile and get configuration "
        self.notifier.notify(self.notifier.event)
        makefile = None
        for file in MakefileNames:
            if os.path.exists(file) and os.path.isfile(file):
                makefile = file

        if not makefile:
            logger.error("makefile doesn't exist")
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
                    relative_root = (line.split("=")[1]).strip()

                    osp_root = os.path.normpath(os.path.join(os.getcwd(), relative_root))
                    self.ide["common"]["root"] = osp_root.replace("\\", "/")
                    self.ide["common"]["folder"] = os.path.relpath(os.getcwd(), osp_root).replace("\\", "/").strip("../")

        return build_template

    def _get_project_conf_template(self):
        cproject_template = self._get_cproject_template()
        build_template = self._get_build_template()

        make_tool = "make"
        if build_template["TOOLCHAIN"] == "mw":
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
                    build_template["APPL"] = (opt_line.split(":")[1]).strip()
                if opt_line.startswith("BOARD"):
                    build_template["BOARD"] = (opt_line.split(":")[1]).strip()
                if opt_line.startswith("BD_VER"):
                    build_template["BD_VER"] = (opt_line.split(":")[1]).strip()
                if opt_line.startswith("CUR_CORE"):
                    build_template["CUR_CORE"] = (opt_line.split(":")[1]).strip()
                if opt_line.startswith("TOOLCHAIN"):
                    build_template["TOOLCHAIN"] = (opt_line.split(":")[1]).strip()
                if opt_line.startswith("EMBARC_ROOT"):
                    relative_root = (opt_line.split(":")[1]).strip()
                    osp_root = os.path.normpath(os.path.join(os.getcwd(), relative_root))
                    self.ide['common']['osp_root'] = os.path.basename(osp_root)
                if  opt_line.startswith("COMPILE_OPT") == True:
                    compile_opt_line = opt_line.split(":")[1]
                    compile_opts = compile_opt_line.split()
        self.notifier.event["message"] = "Get inculdes and defines "
        self.notifier.notify(self.notifier.event)
        if compile_opts != "" and relative_root != "":
            for comp_opt in compile_opts:
                if comp_opt.startswith("-I") == True:
                    inc_path = comp_opt.replace("-I", "", 1)
                    inc_path = os.path.normpath(os.path.join(os.getcwd(), inc_path))

                    includes.append(os.path.relpath(inc_path, relative_root))
                if comp_opt.startswith("-D") == True:
                    define = comp_opt.replace("-D", "", 1)

                    define = define.replace('\\"', '&quot;')
                    define = define.replace('"', '&quot;')

                    cproject_template["defines"].append(define)

        build_template = self. _get_makefile_config(build_template)
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
        self.ide["common"]["name"] = build_template["APPL"] + "_ide"

        for core, settings in CORES.items():
            if cur_core == core:
                cproject_template["core"] = {core: settings}

        for core, settings in cproject_template["core"].items():
            core_id = random.randint(1000000000, 2000000000)
            cproject_template["core"][core]["id"] = core_id

        for path in includes:
            include = os.path.join(self.ide['common']["name"], self.ide['common']['osp_root'], path)
            if path == self.ide['common']["folder"]:
                include = path
            cproject_template["includes"].append(include)
        build_opt_list = ["%s=%s" % (key.upper(), value) for (key, value) in build_template.items()]
        cproject_template["build"] = " ".join(build_opt_list) + " all"
        cproject_template["clean"] = " ".join(build_opt_list) + " clean"
        self.ide["toolchain"] = build_template["TOOLCHAIN"]

        return cproject_template

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

        self.get_asm_c_include()
        outdir = "."
        if "path" in self.ide["common"]:
            app_path = self.ide["common"]["folder"]
            path_depth = len(app_path.split("/"))
            path_list = [app_path.rsplit("/", i)[0] for i in range(path_depth, 0, -1)]

            self.ide["common"]["path_list"] = uniqify(path_list)

        exporter = Exporter("toolchain")
        self.notifier.event["format"] = "string"
        self.notifier.event["message"] = "Start to generate ide files .project and .cproject accroding to templates"
        self.notifier.notify(self.notifier.event)
        exporter.gen_file_jinja("project.tmpl", self.ide["common"], ".project", outdir)
        exporter.gen_file_jinja(".cproject.tmpl", self.ide["exporter"], ".cproject", outdir)
        self.notifier.event["message"] = "Finish generate ide files and they are in " + os.path.abspath(outdir)
        self.notifier.notify(self.notifier.event)