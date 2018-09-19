from __future__ import print_function, division, absolute_import
from tools.download_manager import generate_yaml, edit_yaml, getcwd
from tools.settings import *
from tools.osp import repo
import os
import yaml
help = "Set embarc osp"

def run(args):
    osp_path = OSP()
    url = args.url
    path = args.local
    zip_path = args.zip

    if args.list:
        osp_path.list_path("url")
        osp_path.list_path("local")
        osp_path.list_path("zip")
    if args.set:
        if not(url or path or zip_path):
            print("Please input set one parameter of [url, path, local]")
            return
        if url:
            osp_path.set_path("url", url)
        if path:
            osp_path.set_path("local", path)
        if zip_path:
            osp_path.set_path("zip", zip_path)
    if args.clone:
        osprepo = repo.Repo.fromurl("https://github.com/foss-for-synopsys-dwc-arc-processors/embarc_osp")
        if not path:
            path = getcwd()
        osprepo.clone(osprepo.url,path=os.path.join(path,osprepo.name), rev=None, depth=None, protocol=None, offline=False)

def setup(subparser):
    subparser.add_argument(
        "--clone", action="store_true", help="List osp path")
    subparser.add_argument(
        "--list", action="store_true", help="List osp path")
    subparser.add_argument(
        "--set", action="store_true", help="Set osp path")
    subparser.add_argument(
        "--url", help="OSP git url")
    subparser.add_argument(
        "--zip", help="OSP zip path")
    subparser.add_argument(
        "--local", help="OSP local path")

class OSP(object):
    def __init__(self, file="osp.yaml"):
        self.path = os.path.join(os.path.expanduser("~"), '.embarc_cli')
        if not os.path.exists(self.path):
            try:
                os.mkdir(self.path)
            except (IOError, OSError):
                pass
        self.file = file
        
        fl = os.path.join(self.path, self.file)
        if not os.path.exists(fl):
            self.cfg_dict = dict()
            self.cfg_dict["path"] = dict()
            generate_yaml(fl, self.cfg_dict)
        else:
            self.cfg_dict = yaml.load(fl)

    def set_path(self, var, val):
        fl = os.path.join(self.path, self.file)
        try:
            with open(fl) as f:
                self.cfg_dict = yaml.load(f)
                if "path" in self.cfg_dict:
                    if var in self.cfg_dict["path"]:
                        self.cfg_dict["path"][var].append(val)
                    else:
                        self.cfg_dict["path"][var] = [val]
                        edit_yaml(fl, self.cfg_dict)

        except IOError:
            raise IOError("Can not open file %s ." % fl)

    def list_path(self, var=None):
        fl = os.path.join(self.path, self.file)
        try:
            with open(fl) as f:
                self.cfg_dict = yaml.load(f)
                if var:
                    if "path" in self.cfg_dict:
                        if var in self.cfg_dict["path"]:
                            print("{} :\n {}".format(var, self.cfg_dict["path"][var]))
                        else:
                            print("{} is not exists".format(var))
                    return None

        except IOError:
            raise IOError("Can not open file %s ." % fl)
