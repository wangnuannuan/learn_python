from ide_generator.utils import merge_recursive
class Ide:
    def __init__(self, name, project_dicts):
        assert type(project_dicts) is list, "Project records/dics must be a list" % project_dicts
        self.name = name
        self.ide = {}
        self.ide["common"] = {}
        self.ide["olevel"] = []
        self.ide["common"] = self._get_project_file_template(self.name)
        for project_data in project_dicts:
            if project_data:
                if "common" in project_data:
                    self._set_project_attributes("common", self.ide['common'], project_data)
        print(self.ide["common"]) #what project.tpml need

    def _get_project_file_template(self, name="Default"):
        project_template = {
            "name": name,
            "sources": [],
            "path":""
        }
        return project_template

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



