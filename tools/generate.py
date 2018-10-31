from __future__ import print_function, absolute_import
import os
import logging
import yaml
from tools.utils import load_yaml_records, uniqify, flatten, merge_recursive
from tools.project import Ide

class Generator:

    def generate(self, name=""):

        yield Ide()

