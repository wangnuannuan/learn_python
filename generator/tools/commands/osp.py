from __future__ import print_function, division, absolute_import
from tools.osp import repo, osp
import os
from tools.download_manager import getcwd

help = "Set embarc osp"

def run(args):
    osp_path = osp.OSP()
    url = args.url
    path = args.local
    zip_path = args.zip

    if args.list:
        osp_path.list_path()
    if args.clone:
        url = "https://github.com/foss-for-synopsys-dwc-arc-processors/embarc_osp"
        osprepo = repo.Repo.fromurl(url)
        if not path:
            path = getcwd()
        osprepo.clone(osprepo.url, path=os.path.join(path, osprepo.name), rev=None, depth=None, protocol=None, offline=False)
        osp_path.set_path(osprepo.url, path)

def setup(subparser):
    subparser.add_argument(
        "--clone", action="store_true", help="List osp path")
    subparser.add_argument(
        "--list", action="store_true", help="List osp path")
    subparser.add_argument(
        "--url", help="OSP git url")
    subparser.add_argument(
        "--zip", help="OSP zip path")
    subparser.add_argument(
        "--local", help="OSP local path")



