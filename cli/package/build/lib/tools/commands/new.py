from __future__ import print_function, absolute_import
import os
from tools.osp import (formaturl, repo)
from tools.download_manager import mkdir, getcwd
from tools.osp import repo
from ..template import template
from tools.settings import *

help = "Create a new application"


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
    template.render_makefile(config, application)


def build_config():
    osp_root = raw_input("osp root:")
    board = None
    bd_ver = None
    cur_core = None
    olevel = None
    config = dict()

    if os.path.exists(osp_root) and os.path.isdir(osp_root):
        pass
    else:
        mkdir(osp_root)
        url = "https://github.com/foss-for-synopsys-dwc-arc-processors/embarc_osp"
        repo = repo.Repo.fromurl(url)
        repo.clone(url,path=osp_root, rev=None, depth=None, protocol=None, offline=False)
        repo.sync()
        repo.write()
    config["osp_root"] = os.path.abspath(osp_root)

    print("Support boards {} ".format(SUPPORTED_BOARDS))
    while True:
        board = raw_input("Chose BOARD:")
        if board not in SUPPORTED_BOARDS:
            continue
        else:
            break
    config["board"] = board
    support_bd_ver = BOARD_VERSION[board]
    print("Support board version {} ".format(support_bd_ver))
    while True:
        bd_ver = raw_input("Chose BOARD VERSION:")
        if bd_ver not in support_bd_ver:
            continue
        else:
            break
    config["bd_ver"] = bd_ver

    support_core = SUPPORTED_CORES[board][bd_ver]
    print("Support cores {} ".format(support_core))
    while True:
        cur_core = raw_input("Chose CORE:")
        if cur_core not in support_core:
            continue
        else:
            break
    config["cur_core"] = cur_core
    support_olevel = OLEVEL
    print("Support olevel {}".format(support_olevel))
    while True:
        olevel = raw_input("Chose OLEVEL:")
        if olevel not in support_olevel:
            continue
        else:
            break
    config["olevel"] = olevel
    return config

def setup(subparser):
    subparser.add_argument(
        "-a", "--application", help="Application to be created")
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