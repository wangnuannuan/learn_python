from __future__ import print_function, division, absolute_import
from tools.settings import GNU_PATH, MW_PATH, SUPPORT_TOOLCHAIN, CURRENT_PLATFORM
from distutils.spawn import find_executable
import os
from tools.toolchain import windows_env_set_arc
from tools.cmd import popen
from .. download_manager import getcwd, delete_dir_files

TOOLCHAIN_PATHS = {
    "gnu": GNU_PATH,
    "mw": MW_PATH
}

class ProcessException(Exception):
    pass

class arcToolchain:

    def check_executable(self, tool_key, executable_name):
        '''tool_key: toolchain name
        executable_name: command like ['arc-elf32-gcc', 'ccac']
        return True if the command is supported'''
        if not self.is_supported(tool_key):
            return False
        else:
            try:
                exe = find_executable(executable_name)
                if not exe:
                    print("can not execuate {}".format(executable_name))
                    return False
                toolchian_path = os.path.split(exe)
                TOOLCHAIN_PATHS[tool_key] = toolchian_path
                return True
            except Exception as e:
                print(e)
                return False

    @staticmethod
    def is_supported(tool_key):
        '''check if tool_key is supported'''
        if tool_key not in SUPPORT_TOOLCHAIN:
            print("This toolchian is not supported")
            return False
        else:
            return True

    @staticmethod
    def get_platform():
        return CURRENT_PLATFORM

    def set_toolchain_env(self, tool_key, toolchain_root):
        '''set toolchian's environmental variable
        tool_key: toolchian name "mw" or "gnu"
        toolchian_root: if current platform is windows, this is the bin path ,if current platform is Linux,this should be the root directory
        return False if failed
        '''
        platform = self.get_platform()
        if platform  == "Windows":
            env_obj = windows_env_set_arc.Win32Environment(scope="user")
            windows_env_set_arc.set_env_path(env_obj,'Path', toolchain_root)
            return True
        elif platform  == "Linux":
            file_path = os.path.dirname(os.path.abspath(__file__))
            work_path = getcwd()
            sh_script = os.path.join(file_path, "linux_env_set_arc.sh")
            command = ["bash", sh_path, "-t", tool_key, "-r", toolchain_root]
            try:
                popen(command)
                if "arctool.env" not in  os.listdir(work_path):
                    print("arctool.env doesn't exist")
                    return False
                else:
                    source_command = ["source", "arctool.env"]
                    popen(source_command)
                    try:
                        delete_dir_files("arctool.env")
                    except Exception as e:
                        print(e)
                        return False
                    return True
            except Exception as e:
                print(e)
                return False
        else:
            print("this platform {} is not supported".format(platform))
            return False



