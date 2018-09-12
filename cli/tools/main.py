from __future__ import print_function, absolute_import
import argparse
import os
import pkg_resources
from tools.commands import new#, build
subcommands = {
    "new": new,
    #"build": build,
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', dest='verbosity', action='count', default=0,
        help='Increase the verbosity of the output (repeat for more verbose output)')
    parser.add_argument('-q', dest='quietness', action='count', default=0,
        help='Decrease the verbosity of the output (repeat for more verbose output)')
    parser.add_argument("--version", action='version',
        version=pkg_resources.require("project_generator")[0].version, help="Display version")
    subparsers = parser.add_subparsers(help='commands')

    for name, module in subcommands.items():
        subparser = subparsers.add_parser(name, help=module.help)

        module.setup(subparser)
        subparser.set_defaults(func=module.run)

    args = parser.parse_args()
    verbosity = args.verbosity - args.quietness
    return args.func(args)

if __name__ == '__main__':
    main()
