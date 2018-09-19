from __future__ import print_function, division, absolute_import
from tools.download_manager import getcwd, cd
from tools.settings import *
from tools.cmd import pquery, popen
import os
help = "Show application config"

def run(args):
    root = getcwd()
    app_path = None

    if not args.application:
        app_path = root
    else:
        app_path = os.path.join(root, args.application)
    makefile = get_makefile(app_path)

    if makefile:
        cd(app_path)
        try:
            exe = pquery(["make", "opt"])
            if exe:
                print(exe)
        except Exception as e:
            print(e)
        cd(root)

def get_makefile(app_path):
    for makefile in MakefileNames:
        makefile_path = os.path.join(app_path, makefile)
        if os.path.exists(makefile_path) and os.path.isfile(makefile_path):
            return makefile_path
    return None

def setup(subparser):
    subparser.add_argument(
        "-a", "--application", help="Application path")


