import os
import logging

help = 'Generate a project record'

def run(args):

    if args.project:


def setup(subparser):
    subparser.add_argument(
        "-p", "--project", help="Project to be generated", default = '')
    subparser.add_argument(
        "-t", "--toolchain", help="Create project files for provided toolchain")
       
