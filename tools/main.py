from __future__ import print_function, absolute_import
import argparse
import os, sys
import pkg_resources
from tools.commands import new, showconfig, build, show, toolchain, osp, ide
subcommands = {
    "new": new,
    "appconfig":showconfig,
    "build": build,
    "list": show,
    "toolchain": toolchain,
    "osp": osp,
    "ide": ide,
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', dest='verbosity', action='count', default=0,
        help='Increase the verbosity of the output (repeat for more verbose output)')
    parser.add_argument('-q', dest='quietness', action='count', default=0,
        help='Decrease the verbosity of the output (repeat for more verbose output)')
    parser.add_argument("--version", action='version',
        version=pkg_resources.require("embarc_cli")[0].version, help="Display version")
    subparsers = parser.add_subparsers(help='commands')

    for name, module in subcommands.items():
        subparser = subparsers.add_parser(name, help=module.help)

        module.setup(subparser)
        subparser.set_defaults(func=module.run)
    args = None

    argv_list = list()
    if sys.argv[1] == "build":
        make_list = list()
        for argv in sys.argv[1:]:
            if "=" in argv:
                make_list.append(argv)
            else:
                argv_list.append(argv)
        if len(make_list) > 0 :
            make_config = " ".join(make_list)
            argv_list.extend(["--make", make_config])
        args = parser.parse_args(argv_list)
    else:
        args = parser.parse_args()

    verbosity = args.verbosity - args.quietness
    return args.func(args)

if __name__ == '__main__':
    main()
