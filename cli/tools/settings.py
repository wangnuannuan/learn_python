import platform
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
GNU_PATH = ""
MW_PATH = ""
SUPPORT_TOOLCHAIN = ["gnu", "mw"]
OSP_PATH = ""
CURRENT_PLATFORM = platform.system()