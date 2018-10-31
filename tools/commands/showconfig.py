from __future__ import print_function, division, absolute_import
from tools.download_manager import getcwd, cd
from tools.settings import *
from tools.utils import pquery, popen
import os
from tools.notify import TerminalNotifier
from ..builder import build
help = "Show application config"
notifier = TerminalNotifier()
def run(args):
    root = getcwd()
    app_path = None

    if not args.application:
        app_path = root
    else:
        app_path = os.path.join(root, args.application)
    makefile = get_makefile(app_path)
    if not args.verbose:
        builder = build.embARC_Builder()
        build_config_template = builder.get_build_template()
        builder.get_makefile_config(build_config_template)
    else:
        if makefile:
            with cd(app_path):
                try:
                    exe = pquery(["make", "opt"])
                    if exe:

                        opt_lines = exe.splitlines()

                        table_head = [" ", opt_lines[0].strip("=")]
                        table_content = list()
                        for opt_line in opt_lines:
                            table_line = opt_line.split(":", 1)
                            if len(table_line) > 1:
                                if table_line[0].strip() in ["COMPILE_OPT","ASM_OPT","LINK_OPT", "DBG_HW_FLAGS", "CXX_COMPILE_OPT"]:
                                    table_line_list = table_line[1].split(" ")
                                    for i in range(len(table_line_list)):
                                        table_line_list[i] = table_line_list[i].replace("-I", "include: ")
                                        table_line_list[i] = table_line_list[i].replace("-D", "defines: ")
                                    table_line_list_str = "\n".join(table_line_list)
                                    table_line[1] = table_line_list_str
                                    table_line = [table_line[0], table_line[1]]
                                table_content.append(table_line)

                        notifier.event["format"] = "table"
                        notifier.event["message"] = [table_head, table_content]
                        notifier.notify(notifier.event)
                except Exception as e:
                    print(e)

def get_makefile(app_path):
    for makefile in MakefileNames:
        makefile_path = os.path.join(app_path, makefile)
        if os.path.exists(makefile_path) and os.path.isfile(makefile_path):
            return makefile_path
    return None

def setup(subparser):
    subparser.add_argument(
        "-a", "--application", help="Application path")
    subparser.add_argument(
        "--verbose", action="store_true", help="Show config in detail")

