from __future__ import print_function, absolute_import, unicode_literals

from embarc_tools.download_manager import getcwd
import yaml
from functools import reduce
import operator
import subprocess
import errno

def uniqify(_list):
    return reduce(lambda r, v: v in r[1] and r or (r[0].append(v) or r[1].add(v)) or r, _list, ([], set()))[0]

def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])


def load_yaml_records(yaml_files):
    dictionaries = []
    for yaml_file in yaml_files:
        try:
            f = open(yaml_file, 'rt')
            dictionaries.append(yaml.load(f))
        except IOError:
           raise IOError("The file %s referenced in main yaml doesn't exist." % yaml_file)
    return dictionaries

def merge_recursive(*args):
    if all(isinstance(x, dict) for x in args):
        output = {}
        keys = reduce(operator.or_, [set(x) for x in args])

        for key in keys:
            # merge all of the ones that have them
            output[key] = merge_recursive(*[x[key] for x in args if key in x])

        return output
    else:
        return reduce(operator.add, args)

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
