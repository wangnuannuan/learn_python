from __future__ import print_function, division, absolute_import
from tools.settings import *

help = "Build application"


def run(args):
	if args.board:
		print("support board: {}".format(SUPPORTED_BOARDS))
	if args.bd_ver:
		print("support board version: ")
		for (k ,v)in BOARD_VERSION.items():
			print("{}  support:  {}".format(k, v))
	if args.core:
		print("support cores: ")
		for (k, v) in SUPPORTED_CORES.items():
			for (version, cores) in v.items():
				print("board: {}".format(k))
				print("board version: {}".format(version))
				print("cores: {}".format(cores))
	if args.middleware:
		print("support middlewares: {} ".format(MIDDLEWARE))
	if args.libraries:
		print("support libraries {}".format(LIBRARIES))


def setup(subparser):
	subparser.add_argument(
		"--board", help="List support boards")
	subparser.add_argument(
		"--bd_ver", help="List support board versions")
	subparser.add_argument(
		"--core", help="List support cores")
	subparser.add_argument(
		"--toolchain", help="List support toolchains")
	subparser.add_argument(
		"--middleware", help="List support middlewares")
	subparser.add_argument(
		"--libraries", help="List support libraries")