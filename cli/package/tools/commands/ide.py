from __future__ import print_function, division, absolute_import
from tools.project import Ide
from tools.generate import Generator

help = "Ide generator"



#generator = Ide("baremetal_arc_feature_cache","projects.yaml")
def run(args):
	print("generate")
	if args.generate:
		generator = Generator()
		for project in generator.generate():#"baremetal_arc_feature_cache"
		    project.generate("test")


    
def setup(subparser):
    subparser.add_argument(
        "-g", "--generate", action="store_true", help="Application to be created")

