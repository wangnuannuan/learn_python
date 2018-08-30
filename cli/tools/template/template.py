from __future__ import print_function, absolute_import
from jinja2 import Environment, PackageLoader, FileSystemLoader
import os
from .. download_manager import (getcwd, cd, hide_progress)



def dict_to_list(config):
	'''convert a dict to a list, and it\'s item is tuple'''
	key_list = list(config.keys())
	value_list = list(config.values())
	dest_list = zip(key_list, value_list)
	return dest_list

def render_makefile(config, path=None):
	'''generate a makefile
	config -  a dict and the key should be appl,olevel,board,bd_ver,cur_core,toolchian,osp_root
	path - the makefile will be generated and put in this path
	return True if there is no error'''
	file_path = os.path.dirname(os.path.abspath(__file__))

	if path is None:
		path = getcwd()
	makefile_path = os.path.join(path, "makefile")
	if os.path.exists(file_path):
		env = Environment(loader=PackageLoader("tools.template",'templates'))
		template = env.get_template("makefile.yml")
		template_info = dict_to_list(config)
		content = template.render(template_info)
		with open(makefile_path, "w") as file:
			file.write(content)
		return True
	else:
		print("can not create makefile ,there is no template")
		return False
