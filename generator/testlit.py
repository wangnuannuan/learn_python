import string
import os
import shutil
import random
import getopt
import sys
import commands
import datetime
from cmd import pquery

build_opt = "BOARD=emsk BD_VER=11 CUR_CORE=arcem4 TOOLCHAIN=gnu OUT_DIR_ROOT=${ProjDirPath} all"
build_opt_cells=build_opt.split()
embARC_example_buildopt=" "
make_tool="make"
for opt_cell in build_opt_cells:
    if opt_cell != "all" and "OUT_DIR_ROOT=" not in opt_cell:
        embARC_example_buildopt += " " + opt_cell
    if "TOOLCHAIN=mw" == opt_cell:
        make_tool="gmake"
buildcommand = [make_tool]
setting = embARC_example_buildopt.split()
setting.append("opt")
for i in setting:
    buildcommand.append(i)
print buildcommand

c_includes=""
asm_includes=""
c_defines=""
asm_defines=""
make_cmd = "make"
time_pre = datetime.datetime.now()
cmd_output = pquery(buildcommand)
time_after = datetime.datetime.now()
time_compile = str((time_after-time_pre).seconds)
print "Time Cost:"+time_compile

print cmd_output
compile_opts=""
embARC_root=""
mkfile_loc="."
prj_name = os.path.basename(os.getcwd())
if cmd_output:
    opt_lines=cmd_output.splitlines()
    for opt_line in opt_lines:
        if  opt_line.startswith("COMPILE_OPT") == True:
            compile_opt_line=opt_line.split(":")[1]
            compile_opts=compile_opt_line.split()
        if opt_line.startswith("EMBARC_ROOT") == True:
            embARC_root=opt_line.split(":")[1]

inc_paths=list()
all_defines=list()
### get includes paths and macros
if compile_opts != "" and embARC_root != "":
    for comp_opt in compile_opts:
        if comp_opt.startswith("-I") == True:
            inc_path=comp_opt.replace("-I", "", 1)
            inc_path=embARC_root+"/"+mkfile_loc+"/"+inc_path
            inc_paths.append(os.path.relpath(inc_path, embARC_root))
        if comp_opt.startswith("-D") == True:
            define=comp_opt.replace("-D", "", 1)
            define=define.replace('\\"', '&quot;')
            define=define.replace('"', '&quot;')
            all_defines.append(define)

# print inc_paths
# print all_defines
### Fill the replace string
# Todo : ugly method for tab the includes and marcos
##
for inc_path in inc_paths:
    inc_path="&quot;${workspace_loc:/"+prj_name+"/"+inc_path+"}&quot;"
    c_includes+='<listOptionValue builtIn="false" value="$$"/>'.replace("$$", inc_path) \
    +"\n                                    "
for define in all_defines:
    c_defines+='<listOptionValue builtIn="false" value="$$"/>'.replace("$$", define) \
    +"\n                                    "

c_includes=c_includes.strip()
c_defines=c_defines.strip()
asm_includes=c_includes
asm_defines=c_defines
print c_includes
print c_defines
print asm_includes
print asm_defines
dst= "test1.xml"
dst1= "test2.xml"
open(dst, "w").write(c_includes)
open(dst1, "w").write(c_defines)
