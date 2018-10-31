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
    olevel = args.olevel
    config = build_config()
    config["appl"] = application

    notifier.event["message"] = "current configuration "
    notifier.notify(notifier.event)
    notifier.event["format"] = "table"
    table_head = list()
    table_content = list()
    for key, value in config.items():
        table_head.append(key)
        table_content.append(value)
    notifier.event["message"] = [table_head, [table_content]]
    notifier.notify(notifier.event)

    config["olevel"] = olevel
    app_path = os.path.join(getcwd(), application)
    config["osp_root"] = config["osp_root"].replace("\\" , "/")
    config["middleware"] = args.middleware
    config["csrc"] = args.csrc
    config["asmsrc"] = args.asmsrc
    config["include"] = args.include
    config["defines"] = args.defines


    notifier.event["message"] = "start to generate makefile and main.c "
    notifier.notify(notifier.event)
    exporter = Exporter("application")
    exporter.gen_file_jinja("makefile.tmpl", config, "makefile", application)
    exporter.gen_file_jinja("main.c.tmpl", config, "main.c", application)
    notifier.event["message"] = "finish generate makefile and main.c, and they are in " + app_path
    notifier.notify(notifier.event)

def build_config():
    osppath = osp.OSP()
    osppath.list_path()
    input_root = raw_input("choose osp root or set another path as osp root: ")
    board = None
    bd_ver = None
    cur_core = None
    toolchain = None
    config = dict()
    osp_root = osppath.is_osp(input_root)

    if not osp_root:
        notifier.event["format"] = "string"
        notifier.event["type"] = "warning"
        notifier.event["message"] = "what you choose is not a valid osp root"
        notifier.notify(notifier.event)
        osp_root = osppath.get_path()
        if osp_root:
            notifier.event["message"] = "here choose " + osp_root + "as osp root"
            notifier.notify(notifier.event)
        else:
            osppath.clear_path()
            notifier.event["type"] = "default"
            notifier.event["message"] = "please set a valid osp root or download embarc osp first"
            notifier.notify(notifier.event)
            return None
    notifier.event["type"] = "info"
    config["osp_root"] = os.path.abspath(osp_root)
    notifier.event["message"] = "current osp root is: " + osp_root
    notifier.notify(notifier.event)

    support_board = osppath.support_board(osp_root)
    notifier.event["message"] = "support board : {}".format("  ".join(support_board))
    notifier.notify(notifier.event)
    while True:
        board = raw_input("[embarc] choose board: ")
        if board not in support_board:
            notifier.event["message"] = "please choose board from {}" .format(support_board)
            notifier.notify(notifier.event)
            continue
        else:
            break
    config["board"] = board
    support_bd_ver = osppath.get_board_version(osp_root, board)
    notifier.event["message"] = "{} support versions : {}".format(board, "  ".join(support_bd_ver))
    notifier.notify(notifier.event)
    while True:
        bd_ver = raw_input("[embarc] choose board version: ")
        if bd_ver not in support_bd_ver:
            notifier.event["message"] = "please choose version from {}" .format(support_bd_ver)
            notifier.notify(notifier.event)
            continue
        else:
            break
    config["bd_ver"] = bd_ver

    support_core = osppath.get_tcfs(osp_root, board, bd_ver)

    notifier.event["message"] = "{} with versions {} support cores : {}".format(board, bd_ver, "  ".join(support_core))
    notifier.notify(notifier.event)
    while True:
        cur_core = raw_input("[embarc] choose core: ")
        if cur_core not in support_core:
            notifier.event["message"] = "please choose core from {}" .format(support_core)
            notifier.notify(notifier.event)
            continue
        else:
            break
    config["cur_core"] = cur_core
    support_toolchains = SUPPORT_TOOLCHAIN
    notifier.event["message"] = "support toolchains: {}".format("  ".join(support_toolchains))
    notifier.notify(notifier.event)
    while True:
        toolchain = raw_input("[embarc] choose toolchain: ")
        if toolchain not in support_toolchains:
            notifier.event["message"] = "please choose toolchain from {}" .format(support_toolchains)
            notifier.notify(notifier.event)
            continue
        else:
            break
    config["toolchain"] = toolchain
    return config

def setup(subparser):
    subparser.add_argument(
        "-a", "--application", default="helloworld", help="Application to be created")
    subparser.add_argument(
        "-o", "--olevel", default="O3", help="Choose olevel")
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
