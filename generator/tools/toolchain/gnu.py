from __future__ import print_function, division, absolute_import
from tools.toolchain import arcToolchain, ProcessException
from distutils.spawn import find_executable
from tools.utils import pquery
import re
import os
from .. download_manager import (download_file, extract_file, getcwd, mkdir,delete_dir_files)
import shutil
class Gnu(arcToolchain):
    '''
    version: default version is 2017.09
    root_url: from this url to down load gnu
    pack: where the gnu archive is
    executable_name: a command will be used when check gnu
    '''

    version = "2017.09"
    root_url = "https://github.com/foss-for-synopsys-dwc-arc-processors/toolchain/releases/download/arc-"
    pack = None
    path = None
    executable_name = "arc-elf32-gcc"

    def __init__(self):
        exe = find_executable(self.executable_name)
        if exe:
            self.path = os.path.split(exe)[0]
            self.version = self.check_version()

    @staticmethod
    def check_version():
        '''run command "arc-elf32-gcc--version" and return current gnu version'''
        cmd = ["arc-elf32-gcc", "--version"]
        try:
            exe = pquery(cmd)
            if exe is None:
                print("can not execuate {}".format(cmd[0]))
                return None
            version = re.search(r"[0-9]*\.[0-9]*",exe).group(0)
            if version:
                return version
        except ProcessException:
            return None

    def _set_version(self):
        '''get current gnu version and set the self.version'''
        version = self.check_version()
        if version:
            self.version = version

    def download(self, version=None, path=None):
        '''
        version - gnu version
        path - where the gnu package will be stored
        download gnu package and return the package path
        '''
        if version is None:
            version = self.version
        url = self.root_url + version + "-release/arc_gnu_"  + version+ "_prebuilt_elf32_le_linux_install.tar.gz"
        pack_tgz = "arc_gnu_" + version + "_prebuilt_elf32_le_linux_install.tar.gz"
        if path is None:
            path = getcwd()
        gnu_tgz_path = os.path.join(path, "arc_gnu_" + version +"_prebuilt_elf32_le_linux_install.tar.gz")
        if not os.path.exists(path):
            mkdir(path)
        if pack_tgz in os.listdir(path):
            print("gnu tgz already exists")
        else:
            print("url: ",url)
            print("gnu_tgz_path",gnu_tgz_path)
            result = download_file(url, gnu_tgz_path)
            if not result:
                print("download gnu failed")
                gnu_tgz_path = None
        self.pack = gnu_tgz_path
        return gnu_tgz_path

    def extract_file(self, pack=None, path=None):
        '''extract gnu file from pack to path;
        pack - the path of the compressed package
        path - the compressed package is extracted to this path
        return the root path of gnu and set self.path'''
        if pack is None:
            pack = self.pack
        if path is None:
            path = getcwd()
        if pack is None:
            print("please download gnu file first")
            return False

        else:
            version = re.search(r"[0-9]*\.[0-9]*", pack).group(0)
            if version in os.listdir(path):
                delete_dir_files(version, True)
            try:
                gnu_file_path = extract_file(pack, path)
            except Exception as e:
                print(e)
            if gnu_file_path is not None:
                self.path = os.path.join(path, version, "bin")
                shutil.move(gnu_file_path, version)
                return self.path

    def set_env(self, path=None):
        '''set environment'''
        self.set_toolchain_env("gnu", path)












