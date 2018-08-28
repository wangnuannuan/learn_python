from __future__ import print_function, division, absolute_import
from tools.settings import GNU_PATH, MW_PATH, SUPPORT_TOOLCHAIN
from distutils.spawn import find_executable
import os
TOOLCHAIN_PATHS = {
    "gnu": GNU_PATH,
    "mw": MW_PATH
}

class arcToolchain:
	
	def check_executable(self, tool_key, executable_name):
		if not self.is_supported(tool_key):
			return False
		else:
			exe = find_executable(executable_name)
			if not exe:
				return False
			else:
				toolchian_path = os.path.split(exe)
				TOOLCHAIN_PATHS[tool_key] = toolchian_path
				return True

	def is_supported(self, tool_key):
		if tool_key not in SUPPORT_TOOLCHAIN:
			print("This toolchian is not supported")
			return False
		else:
			return True

	def set_toolchain_env(self, tool_key):
		pass



