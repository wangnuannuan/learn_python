from __future__ import print_function, absolute_import
import os
import logging
import yaml
from ide_generator.utils import load_yaml_records, uniqify, flatten, merge_recursive
from ide_generator.project import Ide

class Generator:

    def __init__(self, projects_file):
        if type(projects_file) is not dict:
            try:
                with open(projects_file, "rt") as f:
                    self.projects_dict = yaml.load(f)
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
                    Ide(name, load_yaml_records(uniqify(flatten(records))))
