from __future__ import print_function, division, absolute_import

import re
import sys
from os import getcwd
from os.path import basename

class TerminalNotifier():
    def __init__(self, verbose=False, silent=False, color=False):
        self.event = self._get_event_template()
        self.color = color or COLOR
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
            "color": "default",
            "message": ""
        }
        return event
    def print_string(self, msg, color='default'):
        pass
    def get_output(self):
        return self.output

    def notify(self, event):
        if self.verbose:
            msg = self.print_notify_verbose(event)
        else:
            msg = self.print_notify(event)
        if msg:
            if not self.silent:
                if self.color:
                    self.print_in_color(event, msg)
                else:
                    print(msg)
            self.output += msg + "\n"

    def print_notify(self, event):
        if event['type'] in ('tool_error', 'info'):
            return event['message']

        elif event['type'] == 'cc' and event['severity'] != 'verbose':
            event['severity'] = event['severity'].title()

            if PRINT_COMPILER_OUTPUT_AS_LINK:
                event['file'] = getcwd() + event['file'].strip('.')
                return '[{severity}] {file}:{line}:{col}: {message}'.format(
                    **event)
            else:
                event['file'] = basename(event['file'])
                return '[{severity}] {file}@{line},{col}: {message}'.format(
                    **event)

        elif event['type'] == 'progress':
            event['action'] = event['action'].title()
            event['file'] = basename(event['file'])
            if 'percent' in event:
                format_string = '{action} [{percent:>5.1f}%]: {file}'
            else:
                format_string = '{action}: {file}'
            return format_string.format(**event)

    def print_notify_verbose(self, event):
        if event['type'] == 'info' or (event['type'] == 'cc' and
                                       event['severity'] == 'verbose'):
            return event['message']
        elif event['type'] == 'debug':
            return "[DEBUG] {message}".format(**event)
        elif event['type'] in ('progress', 'cc'):
            return self.print_notify(event)

    COLOR_MATCHER = re.compile(r"(\w+)(\W+on\W+\w+)?")
    def colorstring_to_escapecode(self, color_string):
        match = re.match(self.COLOR_MATCHER, color_string)
        if match:
            return self.COLORS[match.group(1)] + \
                (self.COLORS[match.group(2).strip().replace(" ", "_")]
                 if match.group(2) else "")
        else:
            return self.COLORS['default']

    def print_in_color(self, event, msg):

        if sys.stdout.isatty() and event.get('severity', None) in CLI_COLOR_MAP:
            sys.stdout.write(self.colorstring_to_escapecode(
                CLI_COLOR_MAP[event['severity']]))
            print(msg)
            sys.stdout.write(self.colorstring_to_escapecode('default'))
        else:
            print(msg)
            sys.stdout.write(self.colorstring_to_escapecode('green'))
notify = TerminalNotifier()
notify.print_in_color(event={}, msg="test")

