from __future__ import print_function, division, absolute_import
from tools.download_manager import mkdir, getcwd
from ..builder import build
from tools.download_manager import getcwd, cd
from tools.settings import *
from tools.utils import pquery
from tools.notify import TerminalNotifier
import sys
help = "Build application"
notifier = TerminalNotifier()

def run(args):
    root = getcwd()
    buildopts = dict()
    osproot = None
    curdir = args.outdir
    app_path = None
    build_status = None
    parallel = args.parallel


    if args.path:
        app_path = args.path
    if args.osp:
        osproot = args.osp
    if args.board:
        buildopts["BOARD"] = args.board
    if args.bd_ver:
        buildopts["BD_VER"] = args.bd_ver
    if args.core:
        buildopts["CUR_CORE"] = args.core
    if args.toolchain:
        buildopts["TOOLCHAIN"] = args.toolchain

    builder = build.embARC_Builder(args.osp, buildopts, curdir)

    if args.make:
        make_config = get_config(args.make)
        current_options = builder.buildopts
        make_options = dict()
        make_config_update = list()

        for config in make_config:
            key = config.split("=")

            make_options[key[0]] = key[1]
        current_options.update(make_options)

        for key, value in current_options.items():
            option = "%s=%s" % (key, value)
            make_config_update.append(option)
        builder.make_options = " ".join(make_config_update)

    if args.target:
        #information = builder.get_build_info(app_path)
        if args.target == "elf":
            build_status = builder.build_elf(app_path, parallel=parallel, pre_clean=False, post_clean=False)
        elif args.target == "bin":
            build_status = builder.build_bin(app_path, parallel=parallel, pre_clean=False, post_clean=False)
        elif args.target == "hex":
            build_status = builder.build_hex(app_path, parallel=parallel, pre_clean=False, post_clean=False)
        elif args.target == "clean":
            build_status = builder.clean(app_path)
        elif args.target == "distclean":
            build_status = builder.distclean(app_path)
        elif args.target == "boardclean":
            build_status = builder.boardclean(app_path)
        elif args.target == "info":
            information = builder.get_build_info(app_path)
        elif args.target == "size":
            information = builder.get_build_size(app_path)
        else:
            print("choose right target")



def get_config(config):
    make_configs = dict()
    if type(config) == list:
        if len(config) == 1 and " " in config[0]:
            config = config[0].split(" ")


    else:
        config = config.split(" ")
    return config

def setup(subparser):
    subparser.add_argument(
        "-d", "--path", default=".", help="Application path")
    subparser.add_argument(
        "--outdir", help="Copy all files to this exported directory")
    subparser.add_argument(
        "--osp", help="OSP root path")
    subparser.add_argument(
        "-b", "--board", help="Build using the given BOARD")
    subparser.add_argument(
        "--bd_ver", help="Build using the given BOARD VERSION")
    subparser.add_argument(
        "--core", help="Build using the given CORE")
    subparser.add_argument(
        "--toolchain", help="Build using the given TOOLCHAIN")
    subparser.add_argument(
        "--parallel", action="store_true", help="Build application with -j")
    subparser.add_argument(
        "--target", default="elf", help="Choose build target, default target is elf and options are [elf, bin, hex, size] ")
    subparser.add_argument(
    "--make", nargs='*', help="Build application with config like 'BOARD=emsk BD_VER=11 CORE=arcem4 TOOLCHAIN=gnu")
