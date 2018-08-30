import argparse
from tools.download_manager import (getcwd, cd)
parser = argparse.ArgumentParser(prog='embarc',
    description="Command-line code management tool for embarc osp ",formatter_class=argparse.RawTextHelpFormatter)
subparsers = parser.add_subparsers(title="Commands", metavar="           ")
parser.add_argument("--version", action="store_true", dest="version", help="print version number and exit")
subcommands = {}

# Process handling
def subcommand(name, *args, **kwargs):
    def __subcommand(command):
        aliases = []
        if not kwargs.get('description') and kwargs.get('help'):
            kwargs['description'] = kwargs['help']
        if not kwargs.get('formatter_class'):
            kwargs['formatter_class'] = argparse.RawDescriptionHelpFormatter
        if kwargs.get('hidden_aliases'):
            aliases = kwargs.get('hidden_aliases')
            del kwargs['hidden_aliases']

        subparser = subparsers.add_parser(name, **kwargs)
        subcommands[name] = subparser

        for arg in args:
            arg = dict(arg)
            opt = arg['name']
            del arg['name']

            if isinstance(opt, basestring):
                subparser.add_argument(opt, **arg)
            else:
                subparser.add_argument(*opt, **arg)

        subparser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="Verbose diagnostic output")
        subparser.add_argument("-vv", "--very_verbose", action="store_true", dest="very_verbose", help="Very verbose diagnostic output")

        def thunk(parsed_args):
            argv = [arg['dest'] if 'dest' in arg else arg['name'] for arg in args]
            argv = [(arg if isinstance(arg, basestring) else arg[-1]).strip('-').replace('-', '_')
                    for arg in argv]
            argv = {arg: vars(parsed_args)[arg] for arg in argv
                    if vars(parsed_args)[arg] is not None}

            return command(**argv)

        subparser.set_defaults(command=thunk)

        # set hidden aliases if any
        for alias in aliases:
            subparsers._name_parser_map[alias] = subparsers._name_parser_map[name]

        return command
    return __subcommand

@subcommand('new',
    dict(name='name', help='Destination name'),
    dict(name='--path', action='store_true', help='The root path of this new program.'),
    dict(name='--guide', action='store_true', help='Create programm setp by step.'),
    description=(
        "Creates a new embarc program if executed within a non-program location.\n"))
def new(name, path=None, guide=False):
    work_path = getcwd()
    file_path = os.path.abspath(__file__)

	if path is None:
        path = getcwd()
    cd(path)
    if os.path.exists(name) and os.path.isdir(name):
        print(" Can not create programm %s , a folder has the same name has exists " % (name))
        return False
    template_path = os.path.join(os.path.split(file_path)[0], "template")
    if os.path.exists(template_path): # copy main.c and makefile to programm folder
        copy_file(template_path, path)
    



