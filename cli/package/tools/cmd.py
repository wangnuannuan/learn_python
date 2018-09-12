from __future__ import print_function, absolute_import

import subprocess
import errno
from tools.download_manager import getcwd

class ProcessException(Exception):
    pass

def popen(command, stdin=None, **kwargs):
    # print for debugging

    proc = None
    try:
        proc = subprocess.Popen(command, **kwargs)
    except OSError as e:
        if e.args[0] == errno.ENOENT:
            print(
                "Could not execute \"%s\".\n"
                "Please verify that it's installed and accessible from your current path by executing \"%s\".\n" % (command[0], command[0]), e.args[0])
        else:
            raise e

    if proc and proc.wait() != 0:
        raise ProcessException(proc.returncode, command[0], ' '.join(command), getcwd())

def pquery(command, output_callback=None, stdin=None, **kwargs):
    proc = None
    try:
        proc = subprocess.Popen(command, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    except OSError as e:
        print(e)
        if e.args[0] == errno.ENOENT:
            print(
                "Could not execute \"%s\".\n"
                "Please verify that it's installed and accessible from your current path by executing \"%s\".\n" % (command[0], command[0]), e.args[0])
        else:
            raise e
    if proc is None:
        print(
                "Could not execute \"%s\".\n"
                "Please verify that it's installed and accessible from your current path by executing \"%s\".\n" % (command[0], command[0]), e.args[0])
        return None

    if output_callback:
        line = ""
        while 1:
            s = str(proc.stderr.read(1))
            line += s
            if s == '\r' or s == '\n':
                output_callback(line, s)
                line = ""

            if proc.returncode is None:
                proc.poll()
            else:
                break

    stdout, _ = proc.communicate(stdin)

    if proc.returncode != 0:
        raise ProcessException(proc.returncode, command[0], ' '.join(command), getcwd())

    return stdout.decode("utf-8")
