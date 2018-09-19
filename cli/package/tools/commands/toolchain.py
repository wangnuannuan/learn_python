from __future__ import print_function, division, absolute_import
from ..toolchain import arcToolchain, gnu, metaware
import os
help = "Build application"


def run(args):
    toolchain_class = None
    if args.toolchain == "gnu":
        toolchain_class = gnu.Gnu()
    elif args.toolchain == "mw":
        toolchain_class =  metaware.Mw()
    else:
        print("this toolchain is not supported")
        return
    if toolchain_class:
        if args.check_version:
            result = toolchain_class.check_version()
            if result:
                print("the toolchain verion is: ", result)
            else:
                print("Please install this toolchain")
                return
        if args.install:
            tgz_path = toolchain_class.download(version=args.version, path=args.download_path)
            bin_path = toolchain_class.extract_file(tgz_path, path=args.extract_path)
            toolchain_class.set_env(path=bin_path)


def setup(subparser):
    subparser.add_argument(
        "--toolchain", required=True, default="gnu", help="Choose gnu")
    subparser.add_argument(
        "--check_version", action="store_true", help="Check toolchain version")
    subparser.add_argument(
        "--install", action="store_true", help="Download toolchain")
    subparser.add_argument(
        "--version", help="Download the specified version toolchain")
    subparser.add_argument(
        "--download_path", help="Toolchain file will be download to this path")
    subparser.add_argument(
        "--extract_path", help="Toolchain file will be extracted to this path")
