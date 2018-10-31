from __future__ import print_function, division, absolute_import
from tools.osp import repo, osp
import os
from tools.download_manager import getcwd
from tools.notify import TerminalNotifier

help = "Set embarc osp"
notifier = TerminalNotifier()
def run(args):
    if not any([args.list ,args.clone]):
        notifier.event["type"] = "warning"
        notifier.event["message"] = "please select a parameter [--clone, --list]"
        notifier.notify(notifier.event)
    osp_path = osp.OSP()

    if args.list:
        notifier.event["message"] = "the current recorded path of osp"
        notifier.notify(notifier.event)
        osp_path.list_path()
    if args.clone:
        url = "https://github.com/foss-for-synopsys-dwc-arc-processors/embarc_osp"
        notifier.event["message"] = "clone embarc_osp from (%s)" % url
        notifier.notify(notifier.event)
        osprepo = repo.Repo.fromurl(url)
        if not path:
            path = getcwd()
        osprepo.clone(osprepo.url, path=os.path.join(path, osprepo.name), rev=None, depth=None, protocol=None, offline=False)
        notifier.event["message"] = "finish"
        notifier.notify(notifier.event)
        osp_path.set_path(osprepo.url, path)
        notifier.event["message"] = "set (%s) to user profile osp.yaml" % os.path.join(path, osprepo.name)
        notifier.notify(notifier.event)

def setup(subparser):
    subparser.add_argument(
        "--clone", action="store_true", help="clone embarc_osp")
    subparser.add_argument(
        "--list", action="store_true", help="List osp path")



