from __future__ import print_function, division, absolute_import
from tools.settings import *

help = "Build application"


def run(args):
    if args.board:
        print("support board: {}".format(SUPPORTED_BOARDS))
    if args.bd_ver:
        print("support board version: ")
        for (k ,v)in BOARD_VERSION.items():
            print("{}  support:  {}".format(k, v))
    if args.core:
        print("support cores: ")
        for (k, v) in SUPPORTED_CORES.items():
            for (version, cores) in v.items():
                print("board: {}".format(k))
                print("version: {}".format(version))
                print("cores: {}\n".format(cores))
    if args.toolchain:
        print("support toolchains: {} ".format(SUPPORT_TOOLCHAIN))
    if args.middleware:
        print("support middlewares: {} ".format(MIDDLEWARE))
    if args.libraries:
        print("support libraries {}".format(LIBRARIES))



def setup(subparser):
    subparser.add_argument(
        "--board", action="store_true", help="List support boards")
    subparser.add_argument(
        "--bd_ver", action="store_true", help="List support board versions")
    subparser.add_argument(
        "--core", action="store_true", help="List support cores")
    subparser.add_argument(
        "--toolchain", action="store_true", help="List support toolchains")
    subparser.add_argument(
        "--middleware", action="store_true", help="List support middlewares")
    subparser.add_argument(
        "--libraries", action="store_true", help="List support libraries")
