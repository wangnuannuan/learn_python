from __future__ import print_function, absolute_import
import os
from tools.osp import (formaturl, repo, osp)
from tools.download_manager import mkdir, getcwd
from tools.settings import *
from tools.notify import TerminalNotifier
from tools.exporter import Exporter

help = "Create a new application"
notifier = TerminalNotifier()
###gnu ................................
def run(args):
    application = args.application
    toolchain = args.toolchain
    config = build_config()
    config["appl"] = application
    config["toolchain"] = toolchain
    app_path = os.path.join(getcwd(), application)
    config["osp_root"] = os.path.relpath(config["osp_root"], app_path)
    config["middleware"] = args.middleware
    config["csrc"] = args.csrc
    config["asmsrc"] = args.asmsrc
    config["include"] = args.include
    config["defines"] = args.defines
    exporter = Exporter("application")
    exporter.gen_file_jinja("makefile.tmpl", config, "makefile", application)
    exporter.gen_file_jinja("main.c.tmpl", config, "main.c", application)


def build_config():
    osppath = osp.OSP()
    osppath.list_path()
    osp_root = raw_input("Choose osp root or set another path as osp root: ")
    board = None
    bd_ver = None
    cur_core = None
    olevel = None
    config = dict()

    if not osppath.is_osp(osp_root):
        notifier.event["format"] = "string"
        notifier.event["type"] = "warning"
        notifier.event["message"] = "This is not a valid osp root: " + osp_root +"\n"
        notifier.notify(notifier.event)
        osp_root = osppath.get_path()
        if osp_root:
            notifier.event["message"] = "Set " + osp_root + "as osp root\n"
            notifier.notify(notifier.event)
        else:
            osppath.clear_path()
            notifier.event["type"] = "default"
            notifier.event["message"] = "Please set a valid osp root or download embarc osp first"
            notifier.notify(notifier.event)
            return None

    config["osp_root"] = os.path.abspath(osp_root)
    support_board = osppath.support_board(osp_root)

    print("{}".format("  ".join(support_board)))
    while True:
        board = raw_input("choose board: ")
        if board not in support_board:
            continue
        else:
            break
    config["board"] = board
    support_bd_ver = osppath.get_board_version(osp_root, board)
    print("{} ".format("  ".join(support_bd_ver)))
    while True:
        bd_ver = raw_input("choose board version: ")
        if bd_ver not in support_bd_ver:
            continue
        else:
            break
    config["bd_ver"] = bd_ver

    support_core = osppath.get_tcfs(osp_root, board, bd_ver)
    print("{} ".format("  ".join(support_core)))
    while True:
        cur_core = raw_input("choose core: ")
        if cur_core not in support_core:
            continue
        else:
            break
    config["cur_core"] = cur_core
    support_olevel = OLEVEL
    print("{}".format("  ".join(support_olevel)))
    while True:
        olevel = raw_input("choose olevel: ")
        if olevel not in support_olevel:
            continue
        else:
            break
    config["olevel"] = olevel
    return config

def setup(subparser):
    subparser.add_argument(
        "-a", "--application", required=True, help="Application to be created")
    subparser.add_argument(
        "-t", "--toolchain", default="gnu", help="Choose toolchain")
    subparser.add_argument(
        '-m', '--middleware', action='store', default= "common", help='Choose a middleware')
    subparser.add_argument(
        '--csrc', action='store', default= ".", help='Application source dirs')
    subparser.add_argument(
        '--asmsrc', action='store', default= ".", help='Application source dirs')
    subparser.add_argument(
        '--include', action='store', default= ".", help='Application include dirs')
    subparser.add_argument(
        '--defines', action='store', default= ".", help='Application defines')
