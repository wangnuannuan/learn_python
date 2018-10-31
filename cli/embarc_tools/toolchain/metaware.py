from __future__ import print_function, division, absolute_import, unicode_literals
from embarc_tools.toolchain import arcToolchain
from distutils.spawn import find_executable
from embarc_tools.utils import pquery
import re
import os
from .. download_manager import (download_file, extract_file, getcwd, mkdir,delete_dir_files)

class Mw(arcToolchain):
    version = "2017.09"
    path = None
    executable_name = "ccac"

    def __init__(self):
        exe = find_executable(self.executable_name)
        if exe:
            self.path = os.path.split(exe)[0]
            self.version = self.check_version()

    @staticmethod
    def check_version():
        cmd = ["ccac", "-v"]
        try:
            exe = pquery(cmd)
            version = re.search(r"[0-9]*\.[0-9]*",exe).group(0)
            if version:
                return version
        except Exception as e:
            print(e)
            return None

    def _set_version(self):
        version = self.check_version()
        if version:
            self.version = version

    def download(self, version=None, path=None):
        print("Can not download metaware using cli")
        return

    def extract_file(self, pack=None, path=None):
        '''extract gnu file from pack to path;
        pack - the path of the compressed package
        path - the compressed package is extracted to this path
        return the root path of gnu and set self.path'''
        pass


    def set_env(self, path=None):
        self.set_toolchain_env("mw", path)
