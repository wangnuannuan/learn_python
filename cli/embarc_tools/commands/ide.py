from __future__ import print_function, division, absolute_import, unicode_literals
from embarc_tools.project import Ide, Generator
import os
from embarc_tools.settings import *
from ..download_manager import cd
from ..osp import (osp)
from embarc_tools.notify import TerminalNotifier
help = "Ide generator"

notifier = TerminalNotifier()


#generator = Ide("baremetal_arc_feature_cache","projects.yaml")
def run(args):
    osppath = osp.OSP()
    message = None
    path = None
    if args.project:
        path = args.project
    else:
        path = os.getcwd()
    if os.path.exists(path):
        makefile = osppath.get_makefile(path)
        if not makefile :
            message = "This is not a valid application path"
            notifier.event["format"] = "string"
            notifier.event["type"] = "error"
            notifier.event["message"] = message
            notifier.notify(notifier.event)
            return
        with cd(path):
            project_file = ".project"
            cproject_file = ".cproject"
            if os.path.exists(".project") and os.path.exists(".cproject"):
                while True:
                    yes = get_input("The IDE project already exists, recreate and overwrite the old files [Y/N]  ")
                    if yes in ["yes", "Y",  "y"]:
                        break
                    elif yes in ["no", "n", "N"]:
                        return
                    else:
                        continue

            if args.generate:
                generator = Generator()
                for project in generator.generate():#"baremetal_arc_feature_cache"
                    project.generate()



def setup(subparser):
    subparser.add_argument(
        "-g", "--generate", action="store_true", help="Application to be created")
    subparser.add_argument(
        "-p", "--project", help="Application path")
    subparser.add_argument(
        "--toolchain", help="Application path")
