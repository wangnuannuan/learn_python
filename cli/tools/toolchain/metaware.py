from __future__ import print_function, division, absolute_import
from tools.toolchain import arcToolchain
from distutils.spawn import find_executable
from tools.cmd import pquery
import re
import os
from .. document_manager import (download_file, extract_file, getcwd, mkdir,delete_dir_files)

class Mw(arcToolchain):
	version = "2017.09"
	path = None
	executable_name = "ccac"

	def __init__(self):
		exe = find_executable(self.executable_name)
		if exe:
			self.path = os.path.split(exe)[0]
			self.version = self.get_version()

	@staticmethod
	def get_version():
		cmd = ["ccac", "-v"]
		try:
			exe = pquery(cmd)
			version = re.search(r"[0-9]*\.[0-9]*",exe).group(0)
			if version:
				return version
		except Exception as e:
			print(e)
			return None

	def set_version(self):
		version = self.get_version()
		if version:
			self.version = version

	def download_mw(self, version=None, path=None):
		pass

	def extract_mw_file(self, pack=None, path=None):
		'''extract gnu file from pack to path;
		pack - the path of the compressed package
		path - the compressed package is extracted to this path
		return the root path of gnu and set self.path'''
		pass


	def set_mw_env(self):
		self.set_toolchain_env("gnu")
		print("set env")