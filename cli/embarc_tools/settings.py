from __future__ import print_function, absolute_import, unicode_literals
import platform

OSP_DIRS = ["arc", "board", "device", "inc", "library", "middleware"]
OLEVEL = ["Os", "O0", "O1", "O2", "O3"]
GNU_PATH = ""
MW_PATH = ""
SUPPORT_TOOLCHAIN = ["gnu", "mw"]
OSP_PATH = ""
CURRENT_PLATFORM = platform.system()
python_version = platform.python_version()
MakefileNames = ['Makefile', 'makefile', 'GNUMakefile']
MIDDLEWARE = ["aws", "coap", "common", "fatfs", "http_parser", "ihex", "lwip-contrib", "Lwip", "mbedtls", "mqtt", "ntshell", "openthread", "parson", "u8glib", "wakaama"]
LIBRARIES = ["clib","secureshield"]
CORES = {
    "arcem4": {"description":"ARC EM4 Configuration"},
    "arcem6": {"description":"ARC EM6 Configuration"},
    "arcem6gp": {"description":"ARC EM6 GP Configuration"},
    "arcem7d": {"description":"ARC EM7D Configuration"},
    "arcem9d": {"description":"ARC EM9D Configuration"},
    "arcem11d": {"description":"ARC EM11D Configuration"},
}

def get_input(input_str):
    if python_version.startswith("2"):
        return raw_input(input_str)
    else:
        return input(input_str)
