from __future__ import print_function, absolute_import
import os
import logging
import yaml
from ide_generate.utils import load_yaml_records, uniqify, flatten, merge_recursive

file_folder = os.path.dirname(os.path.abspath(__file__))
default_project_file = os.path.join(file_folder, "projects.yaml")


class Generator:

    def __init__(self, project_file=None):
        if not project_file:
            project_file = default_project_file
        if type(projects_file) is not dict:
            try:
                with open(project_file, "rt") as f:
                    self.project_dict = yaml.load(f)
            except IOError:
                raise IOError("The main progen projects file %s doesn't exist." % projects_file)
        else:
            self.projects_dict = projects_file



    def generate(self, name=""):
        found = False
        if name != "":
            if "projects" in self.projects_dict:
                if name in self.projects_dict['projects'].keys():
                    found = True
                    records = self.projects_dict['projects'][name]
                    yield Project(name, load_yaml_records(uniqify(flatten(records))))
