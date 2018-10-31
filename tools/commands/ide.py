from __future__ import print_function, division, absolute_import
from tools.project import Ide
from tools.generate import Generator
import os
from tools.download_manager import cd
from tools.osp import (osp)
from tools.notify import TerminalNotifier
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
                    yes = raw_input("The ide file already exists, recreate and overwrite the old file [Y/N]  ")
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
