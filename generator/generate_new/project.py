from ide_generator.utils import merge_recursive, uniqify, pquery
from ide_generator.exporter import Exporter
import os
import random
from tools.settings import *
logger = logging.getLogger("ide.project")
class Ide:
    def __init__(self, name):
        self.name = name
        self.ide = {}
        self.ide["common"] = {}
        self.ide["common"] = self._get_project_file_template(self.name)
        self.ide["cproject"] = self._get_project_conf_template()

    def _get_project_file_template(self, name="Default"):
        project_template = {
            "name": name,
            "path":"",
            "workspace_depth": 3,
            "root": "",
            "outdir": "${ProjDirPath}",
        }
        return project_template

    def _get_cproject_template(self):

        cproject_template = {
            "cores": {}, #//duqu
            "includes": [],
            "defines": [],
            "build": "",
            "clean": ""
        }
        cproject_template["cores"] = CORE
        for core, settings in cproject_template["cores"]:
            core_id = random.randint(1000000000, 2000000000)
            cproject_template["cores"]["id"] = core_id
        return cproject_template

    def _get_makefile_config(self):
        build_template = {
            "BOARD": "",
            "BD_VER": ""
            "CUR_CORE": "",
            "TOOLCHAIN": "",
            "APPL": "",
        }
        makefile = None      
        for file in MakefileNames:
            if not(os.path.exists(file) and os.path.isfile(file)):
                logger.error("makefile doesn't exist")
                return None
            else:
                makefile = file
        with open(makefile) as f:
            lines = f.read().splitlines()
            for line in lines:
                if line.startswith("APPL"):
                    build_template["APPL"] = (line.split("=")[1]).split()
                    self.ide['common']["name"] = build_template["APPL"]
                    self.ide['common']["path"] = os.getcwd()
                if line.startswith("BOARD"):
                    build_template["BOARD"] = (line.split("=")[1]).split()
                if line.startswith("BD_VER"):
                    build_template["BD_VER"] = (line.split("=")[1]).split()
                if line.startswith("CUR_CORE"):
                    build_template["CUR_CORE"] = (line.split("=")[1]).split()
                if line.startswith("TOOLCHAIN"):
                    build_template["TOOLCHAIN"] = (line.split("=")[1]).split()
                if line.startswith("EMBARC_ROOT"):
                    relative_root = (line.split("=")[1]).split()
                    self.ide['common']["root"] = relative_root
                    osp_root = os.path.normpath(os.path.join(os.getcwd(), relative_root))
                    self.ide['common']['path'] = oa.path.relpath(os.getcwd(), osp_root)
        return build_template

    def _get_project_conf_template(self):
        cproject_template = self._get_cproject_template()
        build_template = self._get_makefile_config()
        root = self.ide['common']["root"]

        make_tool = "make"
        if build_template["TOOLCHAIN"] == "mw":
            make_tool = "gmake"
        build_opt_list = ["%s=%s" % (key.upper(), value) for (key, value) in build_template.items()]
        cproject_template["build"] = "make " + " ".join(build_opt_list) + "all"
        cproject_template["clean"] = "make " + " ".join(build_opt_list) + "clean"
        compile_opts = ""
        includes = list()
        opt_command = [make_tool]
        opt_command.extend(build_opt_list)
        opt_command.append("opt")
        cmd_output = pquery(opt_command)
        if cmd_output:
            opt_lines = cmd_output.splitlines()
            for opt_line in opt_lines:
                if  opt_line.startswith("COMPILE_OPT") == True:
                    compile_opt_line = opt_line.split(":")[1]
                    compile_opts = compile_opt_line.split()

        if compile_opts != "" and root != "":
            for comp_opt in compile_opts:
                if comp_opt.startswith("-I") == True:
                    inc_path = comp_opt.replace("-I", "", 1)
                    inc_path = os.path.join(root, self.ide['common']['path'], inc_path)
                    includes.append(os.path.relpath(inc_path, root))
                if comp_opt.startswith("-D") == True:
                    define = comp_opt.replace("-D", "", 1)
                    define = define.replace('\\"', '&quot;')
                    define = define.replace('"', '&quot;')
                    cproject_template["defines"].append(define)
        
        for path in includes:
            include = os.path.join(self.ide['common']["name"], path)
            cproject_template["includes"].append(include)

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
        print(self.ide["exporter"])

    def generate(self, outdir):
        if "path" in self.ide["common"]:
            path_depth = len(self.ide["common"]["path"].split("/"))
            path_list = [self.ide["common"]["path"].rsplit("/", i)[0] for i in range(path_depth, 0, -1)]
            path_list.append(self.ide["common"]["path"])
            self.ide["common"]["path_list"] = uniqify(path_list)
        exporter = Exporter(self.ide["toolchain"])
        exporter.gen_file_jinja("project.tmpl", self.ide["common"], ".project", outdir)
        self.get_asm_c_include()
        self.get_asm_c_include("cproject.tmpl", self.ide["exporter"], ".cproject", outdir)