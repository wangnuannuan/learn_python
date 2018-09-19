from tools import cmd
import re
from tools.toolchain import metaware
import os
#exe = cmd.pquery(["arc-elf32-gcc","--version"])
#print exe.split("\n")[0].split(" ")[-3]

#print(re.search(r"[0-9]*\.[0-9]*",exe).group(0))

'''mw = metaware.Mw()
mw.set_version()
print mw.version'''
from tools.osp import repo

'''repo = repo.Repo.fromurl("https://github.com/foss-for-synopsys-dwc-arc-processors/embarc_osp")
print repo.name
print repo.url
print repo.rev
print repo.path
path = repo.Repo.pathtype()
print path

isurl = repo.Repo.isurl("https://github.com/foss-for-synopsys-dwc-arc-processors/embarc_osp")
print isurl.group()
isinsecure = repo.Repo.isinsecure("https://github.com/foss-for-synopsys-dwc-arc-processors/embarc_osp")
print isinsecure'''

'''url = "https://github.com/foss-for-synopsys-dwc-arc-processors/embarc_applications.git"
path = os.getcwd()
repo = repo.Repo.fromurl(url, path=os.getcwd())

print path
print("repo",repo.revtype(repo.rev))
print(repo.rev)
repo.clone(url,path=os.path.join(path,"embarc_applications"), rev=None, depth=None, protocol=None, offline=False)

repo.sync()
repo.write()
print("repo",repo.revtype(repo.rev))'''

#repo.rm_untracked()
'''print(os.path.abspath(__file__))
print(__file__)

from tools.download_manager import copy_file

copy_file()'''
'''from tools.toolchain import gnu
from tools.download_manager import delete_dir_files,untar
import urllib
#delete_dir_files("2018.03",True)
path = os.path.join(os.getcwd(),"arc_gnu_2018.03_prebuilt_elf32_le_linux_install.tar.gz")
path1 =os.path.join(os.getcwd(),"arc_gnu_2018.03_prebuilt_elf32_le_linux_install")
#urllib.urlretrieve("https://github.com/foss-for-synopsys-dwc-arc-processors/toolchain/releases/download/arc-2018.03-release/arc_gnu_2018.03_prebuilt_elf32_be_linux_install.tar.gz",path)
#gnu = gnu.Gnu()
#gnu.extract_file(path)
untar(path,os.getcwd())'''
'''from tools.toolchain import arcToolchain
toolchain=arcToolchain()
toolchain.set_toolchain_env("gnu",".")'''
repo = repo.Repo.fromurl("https://github.com/foss-for-synopsys-dwc-arc-processors/embarc_osp")
print repo.name
print repo.url
print repo.rev
print repo.path
#path = repo.Repo.pathtype()
