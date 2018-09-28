from __future__ import print_function, division, absolute_import
from tools.settings import *
from tools.osp import (osp)
from tools.notify import TerminalNotifier

help = "Build application"

notifier = TerminalNotifier()
def run(args):
    osppath = osp.OSP()
    osp_root = osppath.get_path()
    if osp_root:
        if args.board:
            support_board = osppath.support_board(osp_root)
            print("support board: {}".format(support_board))
        if args.bd_ver:
            print("support board version: ")
            table_head = ["board", "version"]
            table_content = list()
            support_board = osppath.support_board(osp_root)
            for board in support_board:
                bd_ver = osppath.get_board_version(osp_root, board)
                version = " ".join(bd_ver)
                table_content.append([board, version])
            notifier.event["format"] = "table"
            notifier.event["message"] = [table_head, table_content]
            notifier.notify(notifier.event)
        if args.core:
            print("support cores: ")
            table_head = ["board", "version", "cores"]
            table_content = list()
            support_board = osppath.support_board(osp_root)
            for board in support_board:
                bd_ver = osppath.get_board_version(osp_root, board)
                for bd_version in bd_ver:
                    cur_core = osppath.get_tcfs(osp_root, board, bd_version)
                    cores = " ".join(cur_core)
                    table_content.append([board, bd_version, cores])
            notifier.event["format"] = "table"
            notifier.event["message"] = [table_head, table_content]
            notifier.notify(notifier.event)
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
