from __future__ import print_function, division, absolute_import
from ..toolchain import arcToolchain, gnu, metaware
import os
from tools.notify import TerminalNotifier
help = "Build application"
notifier = TerminalNotifier()

def run(args):
    toolchain_class = None
    if args.toolchain == "gnu":
        toolchain_class = gnu.Gnu()
    elif args.toolchain == "mw":
        toolchain_class =  metaware.Mw()
    else:
        notifier.event["type"] = "warning"
        notifier.event["message"] = "the toolchain (%s) you input is not supported" % args.toolchain
        notifier.notify(notifier.event)
        return
    notifier.event["message"] = "current toolchain is (%s) " % args.toolchain
    notifier.notify(notifier.event)
    if toolchain_class:
        if args.check_version:
            result = toolchain_class.check_version()
            if result:
                notifier.event["message"] = "the toolchain verion is (%s) " % result
                notifier.notify(notifier.event)
            else:
                notifier.event["type"] = "warning"
                notifier.event["message"] = "please install (%s)" % args.toolchain
                notifier.notify(notifier.event)
                return
        if args.install:
            notifier.event["message"] = "start to download ( %s with version %s)" % (args.toolchain, args.version)
            notifier.notify(notifier.event)
            tgz_path = toolchain_class.download(version=args.version, path=args.download_path)
            notifier.event["message"] = "start extracting files and installing toolchain"
            notifier.notify(notifier.event)
            bin_path = toolchain_class.extract_file(tgz_path, path=args.extract_path)
            toolchain_class.set_env(path=bin_path)
            notifier.event["message"] = "start setting environmental variable"
            notifier.notify(notifier.event)
            notifier.event["message"] = "(%s) is download in (%s)" % (args.toolchain, bin_path)
            notifier.notify(notifier.event)

def setup(subparser):
    subparser.add_argument(
        "--toolchain", default="gnu", help="Choose gnu")
    subparser.add_argument(
        "--check_version", action="store_true", help="Check toolchain version")
    subparser.add_argument(
        "--install", action="store_true", help="Download toolchain")
    subparser.add_argument(
        "--version", default="2017.09", help="Download the specified version toolchain")
    subparser.add_argument(
        "--download_path", help="Toolchain file will be download to this path")
    subparser.add_argument(
        "--extract_path", help="Toolchain file will be extracted to this path")
