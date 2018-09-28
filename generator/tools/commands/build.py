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


    if args.path:
        app_path = args.path
    if args.osp:
        osproot = args.osp
    else:
        opt_command = ["make", "opt"]
        with cd(app_path):
            output = pquery(opt_command)
            if output:
                opt_lines = output.splitlines()
                for line in opt_lines:
                    if line.startswith("EMBARC_ROOT"):
                        osproot = (line.split(":")[1]).strip()
    if args.make:
        make_config = get_config(args.make)
        target = None
        target_list = ["elf", "bin","hex", "size"]
        for config in make_config:
            for tar in target_list:
                if "=" not in config:
                    if config == tar:
                        target = tar
        if target:
            make_config.pop(target)
        else:
            target = "all"

        builder = build.embARC_Builder(osproot=osproot)
        builder.make_options = " ".join(make_config)
        print(osproot)
        build_status = builder.build_target(app_path, target=target)



    else:
        if args.board:
            if args.board in SUPPORTED_BOARDS:
                buildopts["BOARD"] = args.board
            else:
                print("board not supported")
                return
        if args.bd_ver:
            buildopts["BD_VER"] = args.bd_ver
        if args.core:
            buildopts["CUR_CORE"] = args.core
        if args.toolchain:
            if args.toolchain in SUPPORT_TOOLCHAIN:
                buildopts["TOOLCHAIN"] = args.toolchain
            else:
                print("toolchain is not supported")
        builder = build.embARC_Builder(osproot, buildopts, curdir)
        if args.elf:
            build_status = builder.build_elf(app_path, pre_clean=True, post_clean=True)
        if args.bin:
            build_status = builder.build_bin(app_path, pre_clean=True, post_clean=True)
        if args.hex:
            build_status = builder.build_hex(app_path, pre_clean=True, post_clean=True)
        if args.target:
            target = args.target
            build_status = builder.build_target(app_path, target=target)
        if args.size:
            build_status = builder.get_build_size(app_path)
            print("build size: {} ".format(build_status[build_size]))
        if args.info:
            information = builder.get_build_info(app_path)
            print(information)
    if build_status:
        notifier.event["format"] = "table"
        notifier.event["type"] = "highlight"
        table_head = ["---", "result"]
        table_content = list()
        table_content.append(["command", build_status["build_cmd"]])
        table_content.append(["time", build_status["time_cost"]])
        table_content.append(["pass", build_status["result"]])
        notifier.event["message"] = [table_head, table_content]
        notifier.notify(notifier.event)

        if not build_status["result"]:
            print("build message: {}".format(build_status["build_msg"]))



def get_config(config):
    make_configs = dict()
    if type(config) == list:
        pass
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
        "--elf", action="store_true", help="Build elf")
    subparser.add_argument(
        "--bin", action="store_true", help="Build bin")
    subparser.add_argument(
        "--hex", action="store_true", help="Build hex")
    subparser.add_argument(
        "--size", action="store_true", help="Get build size")
    subparser.add_argument(
        "--info", action="store_true", help="Get build information")
    subparser.add_argument(
        "--target", default=None, help="Build target")
    subparser.add_argument(
    "--make", nargs='*', help="Build application with config like 'BOARD=emsk BD_VER=11 CORE=arcem4 TOOLCHAIN=gnu")
