from __future__ import print_function, division, absolute_import
from tools.download_manager import mkdir, getcwd
from ..builder import build
from tools.download_manager import getcwd, cd
from tools.settings import *

help = "Build application"


def run(args):
	root = getcwd()
	buildopts = dict()
	osproot = None
	curdir = args.outdir
	app_path = None
	build_status = None

	if args.path:
		app_path = args.path
	if args.osp:
		osproot = args.osp
	else:
		osproot = root
	if args.board:
		if args.board in SUPPORTED_BOARDS:
			buildopts["BOARD"] = args.board
		else:
			print("board not supported")
			return
	if args.bd_ver:
		buildopts["BD_VER"] = args.bd_ver
	if args.core:
		buildopts["CUR_CORE"] = args.core
	if args.toolchain:
		if  toolchain in SUPPORT_TOOLCHAIN:
			buildopts["TOOLCHAIN"] = args.toolchain
		else:
			print("toolchain is not supported")
	builder = build.embARC_Builder(osproot, buildopts, curdir)
	if args.elf:
		build_status = builder.build_elf(app_path, pre_clean=True, post_clean=True)
	if args.bin:
		build_status = builder.build_bin(app_path, pre_clean=True, post_clean=True)
	if args.hex:
		build_status = builder.build_hex(app_path, pre_clean=True, post_clean=True)
	if args.target:
		target = args.target
		build_status = builder.build_target(app_path, target=target)
	if args.size:
		build_status = builder.get_build_size(app_path)
		print("build size: ", build_status[build_size])
	if build_status:
		print("build command: ", build_status["build_cmd"])
		print("build_cost: ", build_status["build_cost"])
		print("build message", build_status["build_msg"])

	if args.info:
		information = builder.get_build_info(app_path)
		print(information)


def setup(subparser):
    subparser.add_argument(
        "-d", "--path", required=True, help="Application path")
    subparser.add_argument(
        "--outdir", required=True, help="Copy all files to this exported directory")
    subparser.add_argument(
        "--osp", help="OSP root path")  
    subparser.add_argument(
        "-b", "--board", help="Build using the given BOARD")  
    subparser.add_argument(
        "--bd_ver", help="Build using the given BOARD VERSION")
    subparser.add_argument(
        "--core", help="Build using the given CORE")
    subparser.add_argument(
        "--toolchain", help="Build using the given TOOLCHAIN")
    subparser.add_argument(
        "--elf", action="store_true", help="Build elf")
    subparser.add_argument(
        "--bin", action="store_true", help="Build bin")
    subparser.add_argument(
        "--hex", action="store_true", help="Build hex")
    subparser.add_argument(
        "--size", action="store_true", help="Get build size")
    subparser.add_argument(
        "--info", action="store_true", help="Get build information")
    subparser.add_argument(
        "--target", default="size", help="Build target")
