from ide_generator.utils import merge_recursive, uniqify, pquery
from ide_generator.exporter import Exporter
import os
import random
class Ide:
    def __init__(self, name, project_dicts):
        assert type(project_dicts) is list, "Project records/dics must be a list" % project_dicts
        self.name = name
        self.ide = {}
        self.ide["common"] = {}
        self.ide["cores"] = {}
        self.ide["common"] = self._get_project_file_template(self.name)
        self.ide["settings"] = self._get_project_conf_template()
        self.ide["toolchain"] = "gnu"
        for project_data in project_dicts:
            if project_data:
                if "toolchain" in project_data:
                    self.ide["toolchain"] = project_data["toolchain"][0]
                if "common" in project_data:
                    self._set_project_attributes("common", self.ide['common'], project_data)
                if "settings" in project_data:
                    self._set_project_attributes("settings", self.ide['settings'], project_data)
                if "cores" in project_data:
                    self.ide["cores"] = project_data["cores"]
                    self._set_cores()




        print(self.ide["common"]) #what project.tpml need
        print(self.ide["settings"])
        print(self.ide["cores"])
        print(self.ide["toolchain"])

    def _get_project_file_template(self, name="Default"):
        project_template = {
            "name": name,
            "sources": [],
            "path":"",
            "workspace_depth":"",
            "root": ""
        }
        return project_template

    def _get_cproject_template(self):
        project_template = {
            "includes": [],
            "defines": []
        }
        project_template.update(self.ide["common"])
        for core, settings in self.ide["cores"].items():
            core_id = random.randint(1000000000, 2000000000)
            self.ide["cores"]["id"] = core_id
        return project_template
    def _get_project_conf_template(self):
        settings_template = {
            "board":{},
            "cur_core": "",
            "outdir": "${ProjDirPath}",
            "appl": self.name,
            

        }
        return settings_template
    def _set_cores(self):
        for core , setting in self.ide["cores"].items():
            if "description" in setting:
                if type(setting["description"]) is list:
                    self.ide["cores"][core]["description"] = setting["description"][0]


    def _get_project_olevel_template():
        pass

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
        build_opt = self.ide["settings"]
        board = build_opt["board"].keys()[0]
        boadd_version = build_opt["board"][board][0]
        build_opt["board"] = board
        build_opt["bd_ver"] = boadd_version
        build_opt["cur_core"] = self.ide["cores"].keys()[0]
        build_opt["toolchain"] = self.ide["toolchain"]
        build_opt_list = ["%s=%s" % (key.upper(), value) for (key, value) in build_opt.items()]
        make_tool = "make"
        if self.ide["toolchain"] == "mw":
            make_tool = "gmake"
        build_command = [make_tool]
        build_command.extend(build_opt_list)
        build_command.extend(["all", "opt"])

        appl_path = os.path.join(self.ide["common"]["root"], self.ide["common"]["path"])
        path_work_now = os.getcwd()
        os.chdir(appl_path)
        cmd_output = pquery(build_command)
        os.chdir(path_work_now)
        cproject_template = self._get_cproject_template()
        includes = list()

        compile_opts = ""
        relative_root = ""
        if cmd_output:
            opt_lines = cmd_output.splitlines()
            for opt_line in opt_lines:
                if  opt_line.startswith("COMPILE_OPT") == True:
                    compile_opt_line = opt_line.split(":")[1]
                    compile_opts = compile_opt_line.split()
                if opt_line.startswith("EMBARC_ROOT") == True:
                    relative_root = opt_line.split(":")[1]
        if compile_opts != "" and relative_root != "":
            for comp_opt in compile_opts:
                if comp_opt.startswith("-I") == True:
                    inc_path = comp_opt.replace("-I", "", 1)
                    inc_path = os.path.join(relative_root, self.ide["common"]["path"], inc_path)
                    includes.append(os.path.relpath(inc_path, relative_root))
                if comp_opt.startswith("-D") == True:
                    define = comp_opt.replace("-D", "", 1)
                    define = define.replace('\\"', '&quot;')
                    define = define.replace('"', '&quot;')
                    self.ide['common']["defines"].append(define)
        for path in includes:
            include = os.path.join(self.ide['common']["name"], path)
            cproject_template["includes"].append(include)

        for core, settings in self.ide["cores"].items():
            core_id = random.randint(1000000000, 2000000000)
            self.ide["cores"]["id"] = core_id

        self.ide["exporter"] = dict()
        self.ide["exporter"].update(self.ide["common"])
        self.ide["exporter"]["cores"] = dict()
        self.ide["exporter"]["cores"].update(self.ide['cores'])
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






