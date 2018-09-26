import platform

OSP_DIRS = ["arc", "board", "device", "inc", "library", "middleware"]
SUPPORTED_BOARDS = ["emsk", "axs", "hsdk", "nsim"]

BOARD_VERSION = {"emsk": ["11", "22" ,"23"], "axs": ["103"], "hsdk": ["10"], "nsim": ["10"]}

SUPPORTED_CORES = {
    "emsk" : {"11" : ["arcem4", "arcem4cr16", "arcem6", "arcem6gp"],
        "22" : ["arcem7d", "arcem9d", "arcem11d"],
        "23" : ["arcem7d", "arcem7d_em4", "arcem7d_em5d", "arcem7d_em6", "arcem9d", "arcem9d_em5d", "arcem11d", "arcem11d_em7d"]
    },
    "axs" : {"103" : ["archs36"]},
    "hsdk" : {"10" : ["archs38_c0", "archs38_c1", "archs38_c2", "archs38_c3"]},
    "nsim" : {"10" : ["arcem", "archs", "arcsem"]}

}
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