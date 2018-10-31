from __future__ import print_function, division, absolute_import
from tools.settings import *
from tools.osp import (osp)
from tools.notify import TerminalNotifier

help = "Build application"

notifier = TerminalNotifier()
def run(args):
    osp_root = args.osp
    osppath = osp.OSP()
    if not any([args.board, args.bd_ver, args.core, args.toolchain, args.middleware,args.libraries]):
        notifier.event["type"] = "warning"
        notifier.event["message"] = "please select a parameter [--board --bd_ver --core --toolchain --middleware --libraries]"
        notifier.notify(notifier.event)
        return
    if osp_root:
        if not osppath.is_osp(osp_root):
            osp_root = osppath.get_path()
    if osp_root:
        show = False
        notifier.event["message"] = "here choose " + osp_root + "as osp root"
        notifier.notify(notifier.event)
        if args.board:

            support_board = osppath.support_board(osp_root)
            notifier.event["message"] = "support board : {}".format("  ".join(support_board))
            notifier.notify(notifier.event)
        if args.bd_ver:

            notifier.event["message"] = "support board version"
            notifier.notify(notifier.event)
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

            notifier.event["message"] = "support cores"
            notifier.notify(notifier.event)
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
            notifier.event["message"] = "support toolchain : {}".format("  ".join(SUPPORT_TOOLCHAIN))
            notifier.notify(notifier.event)
        if args.middleware:
            notifier.event["message"] = "support middleware : {}".format("  ".join(MIDDLEWARE))
            notifier.notify(notifier.event)
        if args.libraries:
            notifier.event["message"] = "support libraries : {}".format("  ".join(LIBRARIES))
            notifier.notify(notifier.event)

    else:
        notifier.event["type"] = "warning"
        notifier.event["message"] = "please set a valid osp root [--osp]"
        notifier.notify(notifier.event)

def setup(subparser):
    subparser.add_argument(
        "--osp", default=".", help="Choose a osp root to get configurations")
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
