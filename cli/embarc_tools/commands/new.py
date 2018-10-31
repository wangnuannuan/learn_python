from __future__ import print_function, absolute_import, unicode_literals, unicode_literals
import os
from ..osp import (formaturl, repo, osp)
from ..download_manager import mkdir, getcwd
from embarc_tools.settings import *
from embarc_tools.notify import TerminalNotifier
from embarc_tools.exporter import Exporter
import collections
help = "Create a new application"
notifier = TerminalNotifier()

def run(args):

    olevel = args.olevel
    application = args.application

    if not application:
        while True:
            application = get_input("[embARC] Input application name: ")
            if application == "":
                notifier.event["message"] = "Please don't set applcation name as a empty string "
                notifier.notify(notifier.event)
                application = None
                continue
            else:
                break
    args.application = application
    config = build_config(args)
    # config["APPL"] = application

    notifier.event["message"] = "Current configuration "
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
    config["EMBARC_OSP_ROOT"] = config["EMBARC_OSP_ROOT"].replace("\\" , "/")
    config["middleware"] = args.middleware
    config["csrc"] = args.csrc
    config["asmsrc"] = args.asmsrc
    config["include"] = args.include
    config["defines"] = args.defines
    config["os"] = args.os
    config["lib"] = args.library

    notifier.event["message"] = "Start to generate makefile and main.c "
    notifier.notify(notifier.event)
    exporter = Exporter("application")
    exporter.gen_file_jinja("makefile.tmpl", config, "makefile", application)
    exporter.gen_file_jinja("main.c.tmpl", config, "main.c", application)
    notifier.event["message"] = "Finish generate makefile and main.c, and they are in " + app_path
    notifier.notify(notifier.event)

def build_config(args):
    osppath = osp.OSP()
    osppath.list_path()
    input_root = args.osp_root
    if not input_root:
        input_root = get_input("[embARC] Choose osp root or set another path as osp root: ")
    board = args.board
    bd_ver = args.bd_ver
    cur_core = args.cur_core
    toolchain = args.toolchain
    # config = dict()
    config = {
        "APPL": "",
        "BOARD": "",
        "BD_VER": "",
        "CUR_CORE": "",
        "TOOLCHAIN": "",
        "EMBARC_OSP_ROOT": "",

    }
    config = collections.OrderedDict()
    config["APPL"] = args.application
    osp_root = osppath.is_osp(input_root)

    if not osp_root:
        notifier.event["format"] = "string"
        notifier.event["type"] = "warning"
        notifier.event["message"] = "What you choose is not a valid osp root"
        notifier.notify(notifier.event)
        osp_root = osppath.get_path()
        if osp_root:
            notifier.event["message"] = "Here choose " + osp_root + "as osp root"
            notifier.notify(notifier.event)
        else:
            osppath.clear_path()
            notifier.event["type"] = "default"
            notifier.event["message"] = "Please set a valid osp root or download embarc osp first"
            notifier.notify(notifier.event)
            return None
    notifier.event["type"] = "info"

    notifier.event["message"] = "Current osp root is: " + osp_root
    notifier.notify(notifier.event)

    support_board = osppath.support_board(osp_root)
    notifier.event["message"] = "Support board : {}".format("  ".join(support_board))
    notifier.notify(notifier.event)
    while True:
        if not board:
            board = get_input("[embARC] Choose board: ")
        if board not in support_board:
            board = None
            notifier.event["message"] = "Please choose board from {}" .format(support_board)
            notifier.notify(notifier.event)
            continue
        else:
            break
    config["BOARD"] = board
    support_bd_ver = osppath.get_board_version(osp_root, board)
    notifier.event["message"] = "{} support versions : {}".format(board, "  ".join(support_bd_ver))
    notifier.notify(notifier.event)
    while True:
        if not bd_ver:
            bd_ver = get_input("[embARC] Choose board version: ")
        if bd_ver not in support_bd_ver:
            bd_ver = None
            notifier.event["message"] = "Please choose version from {}" .format(support_bd_ver)
            notifier.notify(notifier.event)
            continue
        else:
            break
    config["BD_VER"] = bd_ver

    support_core = osppath.get_tcfs(osp_root, board, bd_ver)

    notifier.event["message"] = "{} with versions {} support cores : {}".format(board, bd_ver, "  ".join(support_core))
    notifier.notify(notifier.event)
    while True:
        if not cur_core:
            cur_core = get_input("[embARC] choose core: ")
        if cur_core not in support_core:
            cur_core = None
            notifier.event["message"] = "pPease choose core from {}" .format(support_core)
            notifier.notify(notifier.event)
            continue
        else:
            break
    config["CUR_CORE"] = cur_core
    support_toolchains = SUPPORT_TOOLCHAIN
    notifier.event["message"] = "Support toolchains: {}".format("  ".join(support_toolchains))
    notifier.notify(notifier.event)
    while True:
        if not toolchain:
            toolchain = get_input("[embARC] Choose toolchain: ")
        if toolchain not in support_toolchains:
            toolchain = None
            notifier.event["message"] = "Please choose toolchain from {}" .format(support_toolchains)
            notifier.notify(notifier.event)
            continue
        else:
            break
    config["TOOLCHAIN"] = toolchain
    config["EMBARC_OSP_ROOT"] = os.path.abspath(osp_root)
    return config

def setup(subparser):
    subparser.add_argument(
        "-a", "--application", help="Application to be created")
    subparser.add_argument(
        "-b", "--board", help="Choose board")
    subparser.add_argument(
        "--bd_ver", help="Choose board version")
    subparser.add_argument(
        "--cur_core", help="Choose core")
    subparser.add_argument(
        "--toolchain", help="Choose toolchain")
    subparser.add_argument(
        "--osp_root", help="Choose embARC osp root path")
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
    subparser.add_argument(
        '--os', action='store', default= "", help='Choose os')
    subparser.add_argument('--library', action='store', default= "", help='Choose library')
