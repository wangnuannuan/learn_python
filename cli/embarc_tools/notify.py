from __future__ import print_function, absolute_import, unicode_literals

import re
import sys
from prettytable import PrettyTable

COLOR = False
CLI_COLOR_MAP = {
    "info": "white",
    "warning": "yellow",
    "error"  : "red",
    "highlight": "cyan"
}

class TerminalNotifier():

    def __init__(self, color=True):
        self.event = self._get_event_template()
        self.color = color
        self.messages = []
        if self.color:
            from colorama import init, Fore, Back, Style
            init()
            self.COLORS = {
                'none' : "",
                'default' : Style.RESET_ALL,
                'black'   : Fore.BLACK,
                'red'     : Fore.RED,
                'green'   : Fore.GREEN,
                'yellow'  : Fore.YELLOW,
                'blue'    : Fore.BLUE,
                'magenta' : Fore.MAGENTA,
                'cyan'    : Fore.CYAN,
                'white'   : Fore.WHITE,

                'on_black'   : Back.BLACK,
                'on_red'     : Back.RED,
                'on_green'   : Back.GREEN,
                'on_yellow'  : Back.YELLOW,
                'on_blue'    : Back.BLUE,
                'on_magenta' : Back.MAGENTA,
                'on_cyan'    : Back.CYAN,
                'on_white'   : Back.WHITE,
            }

    def _get_event_template(self):
        event = {
            "type": "info",
            "format": "string",
            "message": ""
        }
        return event

    def collect_message(self, message):
        msg = "[embARC] %s\n" % message
        self.messages.append(msg)

    def notify(self, event):
        if event["format"] =="string":
            self.print_string(event)
            return True
        elif event["format"] =="table":
            self.print_table(event)
            return True
        else:
            msg = "Can not display this message"
            event = dict()
            event["message"] = msg
            event["type"] = "warning"
            event["format"] = "string"
            self.print_string(event)
            return False

    def print_string(self, event):
        if event.get("type", None) in CLI_COLOR_MAP: # sys.stdout.isatty() and
            sys.stdout.write(self.colorstring_to_escapecode(
                CLI_COLOR_MAP[event["type"]]))
            print("[embARC] %s\n" % event["message"], end="")
            sys.stdout.write(self.colorstring_to_escapecode('default'))
        self.event["type"] = "info"

    def print_table(self, event):
        if type(event["message"]) is list:
            if len(event["message"]) > 1:
                table_head = event["message"][0]
                table_content = event["message"][1]
                if event.get("type", None) in CLI_COLOR_MAP: #sys.stdout.isatty() and 
                    sys.stdout.write(self.colorstring_to_escapecode(
                        CLI_COLOR_MAP[event["type"]]))
                    pretty_table = PrettyTable(table_head)
                    pretty_table.align = "l"
                    for content in table_content:
                        if len(content) > 0:
                            pretty_table.add_row(content)
                    print(pretty_table)
                    sys.stdout.write(self.colorstring_to_escapecode('default'))

        else:
            msg = "Can not display this message"
            event = dict()
            event["message"] = msg
            event["type"] = "warning"
            event["format"] = "string"
            self.print_string(event)
        self.event["format"] = "string"
        self.event["type"] = "info"

    COLOR_MATCHER = re.compile(r"(\w+)(\W+on\W+\w+)?")


    def colorstring_to_escapecode(self, color_string):
        match = re.match(self.COLOR_MATCHER, color_string)
        if match:
            return self.COLORS[match.group(1)] + \
                (self.COLORS[match.group(2).strip().replace(" ", "_")]
                 if match.group(2) else "")
        else:
            return self.COLORS['default']





