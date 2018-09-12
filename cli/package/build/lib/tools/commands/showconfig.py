from __future__ import print_function, division, absolute_import
from tools.download_manager import getcwd, cd
from tools.settings import *
from tools.cmd import popen
help = "Show application config"

def run(args):
	root = getcwd()
	app_path = args.application
	if not app_path:
		app_path = root
	makefile = get_makefile(app_path)
	if makefile:
		cd(app_path)
		try:
			popen(["make", "opt"])
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


