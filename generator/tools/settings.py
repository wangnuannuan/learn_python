import platform

OSP_DIRS = ["arc", "board", "device", "inc", "library", "middleware"]
OLEVEL = ["Os", "O0", "O1", "O2", "O3"]
GNU_PATH = ""
MW_PATH = ""
SUPPORT_TOOLCHAIN = ["gnu", "mw"]
OSP_PATH = ""
CURRENT_PLATFORM = platform.system()
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
