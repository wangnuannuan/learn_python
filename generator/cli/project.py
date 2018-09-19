from ide_generate.utils import merge_recursive
class IDE:
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

	def _get_project_file_template(self, name="Default"):
		project_template = {
		    "name": name,
		    "sources": []
		    "path":""
		}
		return project_template

	def _set_project_attributes(self, key_values, destination, source): # source --> destination
		if key_values in source:
			for attribute, data in source[key_value].items():
				if attribute in destination:
					if type(destination[attribute]) is list:
						if type(data) is list:
							destination[attribute].extend(data)
						else:
							destination[attribute].append(data)
					elif type(destination[attribute]) is dict:
						destination[attribute] = 




