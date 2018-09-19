import argparse
import os
import logging

import pkg_resources

from .commands import generate

subcommands = {
    'generate': generate,

}

def main():
    # Parse Options
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

    # set the verbosity
    verbosity = args.verbosity - args.quietness

    logging_level = max(logging.INFO - (10 * verbosity), 0)
    logging.basicConfig(format="%(name)s %(levelname)s\t%(message)s", level=logging_level)
    logger = logging.getLogger('progen')

    logger.debug('This should be the project root: %s', os.getcwd())

    return args.func(args)

if __name__ == '__main__':
    main()