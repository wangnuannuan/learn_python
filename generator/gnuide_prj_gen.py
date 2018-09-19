#! /usr/bin/env python
# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import string
import os
import shutil
import random
import getopt
import sys
import commands
import datetime

# workspace of gnu ide relative to embARC source root #
ide_workspace_relative_depth = 3
digilent_debug_server_port = 49105
openocd_bin_path = "C:\\arc_gnu\\bin\openocd.exe"
default_build_conf='arcem6'
new_obj_folder_gen=1
embARC_sourceroot="../../../"

def set_default_build_conf(conf):
	'''set default build conf
	'''
	global default_build_conf
	default_build_conf = conf
	pass

def set_ide_workspace_relative_depth(depth):
	'''set ide workspace relative depth
	'''
	global ide_workspace_relative_depth
	if type(depth) == int:
		ide_workspace_relative_depth = depth
	elif type(depth) == str and depth.isdigit():
		ide_workspace_relative_depth=int(depth)
	pass

def cconfiguration_node_gen(tmpl, xml, prj_name, cfg_name, cfg_desc, mkfile_loc, build_opt, clean_opt, tool_id):
	'''
	Generate GNU IDE cproject cconfiguration xml node using template file
	'''
	c_includes=""
	asm_includes=""
	c_defines=""
	asm_defines=""

	TO_REPLACE_KEYS = ["$PRJ_NAME$", "$CFG_NAME$", "$CFG_DESC$", "$MKFILE_LOC$", "$BUILD_OPT$",\
	 		"$CLEAN_OPT$", "$TOOL_ID$", "$ASM_INCLUDES$", "$ASM_DEFINES$", "$C_INCLUDES$", "$C_DEFINES$"]

	##### Acquire Includes paths and Macros definition using make opt
	embARC_example_path=embARC_sourceroot+mkfile_loc ##makefile example/baremetal/arc_feature/cache
	## Build Options Acquire
	build_opt_cells=build_opt.split()#[BOARD=emsk BD_VER=11 CUR_CORE=arcem4 TOOLCHAIN=gnu OUT_DIR_ROOT=${ProjDirPath} APPL=baremetal_arc_feature_cache all]
	embARC_example_buildopt=" "
	make_tool="make"
	for opt_cell in build_opt_cells:
		if opt_cell != "all" and "OUT_DIR_ROOT=" not in opt_cell:
			embARC_example_buildopt += " " + opt_cell
		if "TOOLCHAIN=mw" == opt_cell:
			make_tool="gmake"

	#print embARC_example_path + embARC_example_buildopt
	make_cmd=make_tool + " --no-print-directory -C " + embARC_example_path + embARC_example_buildopt
	#print make_cmd
	time_pre = datetime.datetime.now()
	(cmd_status, cmd_output)=commands.getstatusoutput(make_cmd+ " opt") #执行 make opt返回 元组tuple(status, result),resut中包含CURRENT CONFIGURATION
	time_after = datetime.datetime.now()
	time_compile = str((time_after-time_pre).seconds)
	print "Time Cost:"+time_compile
	##print cmd_status, cmd_output
	compile_opts=""
	embARC_root=""
	if cmd_status == 0:
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
		inc_path="&quot;${workspace_loc:/"+prj_name+"/"+inc_path+"}&quot;"#####################################################
		c_includes+='<listOptionValue builtIn="false" value="$$"/>'.replace("$$", inc_path) \
		+"\n									"
	for define in all_defines:
		c_defines+='<listOptionValue builtIn="false" value="$$"/>'.replace("$$", define) \
		+"\n									"

	c_includes=c_includes.strip()
	c_defines=c_defines.strip()
	asm_includes=c_includes
	asm_defines=c_defines

	## Fix replaced keys cfg_name arcem6  cfg_desc =#ARC EM6 Configuration build opt BOARD=emsk BD_VER=11 CUR_CORE=arcem4 TOOLCHAIN=gnu OUT_DIR_ROOT=${ProjDirPath} APPL=baremetal_arc_feature_cache all
	REPLACED_KEYS = [prj_name, cfg_name, cfg_desc, mkfile_loc, build_opt, \
			clean_opt, tool_id, asm_includes, asm_defines, c_includes, c_defines]

	ccfg_node_xml_fp = open(xml, 'w+') #gnu/baremetal_arc_feature_cache/cconfs_baremetal_arc_feature_cache.xmlconf_0 aecem6 0 arcem4 1....
	tmpl_reader = open(tmpl, 'r').read() #./templates/gnu/cconfiguration.tmpl
	i = 0
	for key in TO_REPLACE_KEYS: #将./templates/gnu/cconfiguration.tmpl内的字符替换掉写进gnu/baremetal_arc_feature_cache/cconfs_baremetal_arc_feature_cache.xmlconf_0
		tmpl_reader = tmpl_reader.replace(str(key), str(REPLACED_KEYS[i]))
		i = i + 1

	ccfg_node_xml_fp.seek(0)
	ccfg_node_xml_fp.write(tmpl_reader)
	ccfg_node_xml_fp.close()

	pass

def refreshscope_conf_node_gen(tmpl, xml, prj_name, cfg_name):
	'''
	Generate GNU IDE refreshScope configuration node xml using template file
	'''
	TO_REPLACE_KEYS = ["$PRJ_NAME$", "$CFG_NAME$"]
	REPLACED_KEYS = [prj_name, cfg_name]#[ , arcem6] cores的name

	rsf_node_xml_fp = open(xml, 'w+')##gnu/baremetal_arc_feature_cache/rsfs__baremetal_arc_feature_cache.xml
	tmpl_reader = open(tmpl, 'r').read()##./templates/gnu/refresh_configuration.tmpl

	i = 0
	for key in TO_REPLACE_KEYS:
		tmpl_reader = tmpl_reader.replace(str(key), str(REPLACED_KEYS[i]))
		i = i + 1

	rsf_node_xml_fp.seek(0)
	rsf_node_xml_fp.write(tmpl_reader)
	rsf_node_xml_fp.close()
	pass

def cconfiguration_nodes_gen(tmpl, xml, prj_name, **build_confs):
	if build_confs == None: #tmp#./templates/gnu/cconfiguration.tmpl, gnu/baremetal_arc_feature_cache/cconfs_baremetal_arc_feature_cache.xml xml
		return

	build_confs_key_sorted=list() #[arcem6，其他能用的core]
	print "cconfiguration_nodes_gen {}".format(build_confs)
	## add default build conf first ##
	if build_confs.has_key(default_build_conf) == True: # arcem6
		build_confs_key_sorted.append(default_build_conf)
	for build_conf_key in build_confs:
		if build_conf_key != default_build_conf:
			build_confs_key_sorted.append(build_conf_key)

	xml_fp = open(xml, 'w+')# gnu/baremetal_arc_feature_cache/cconfs_baremetal_arc_feature_cache.xml
	xml_fp.seek(0)
	index = 0
	for build_conf in build_confs_key_sorted:
		cfg_name = build_conf
		build_conf_table = build_confs[build_conf].split('<>')
		### build_conf_table ##
		## key_name :     0         1           2          3         4
		## cfg_name : cfg_desc, mkfile_loc, build_opt, clean_opt  tool_id
		#######################
		cfg_desc 	= build_conf_table[0].strip() #ARC EM6 Configuration
		mkfile_loc 	= build_conf_table[1].strip() #example/baremetal/arc_feature/cache
		build_opt 	= build_conf_table[2].strip() #BOARD=emsk BD_VER=11 CUR_CORE=arcem4 TOOLCHAIN=gnu OUT_DIR_ROOT=${ProjDirPath} APPL=baremetal_arc_feature_cache all
		clean_opt 	= build_conf_table[3].strip() #BOARD=emsk BD_VER=11 CUR_CORE=arcem4 TOOLCHAIN=gnu OUT_DIR_ROOT=${ProjDirPath} APPL=baremetal_arc_feature_cache clean
		tool_id		= build_conf_table[4].strip() #随机生成
		cconf_xml_file = xml + 'conf_' + str(index) # gnu/baremetal_arc_feature_cache/cconfs_baremetal_arc_feature_cache.xmlconf_0
		index = index + 1
		# generate one conf xml file,
		# read it and write it to all confs file,
		# then delete the conf file #
		cconfiguration_node_gen(tmpl, cconf_xml_file, prj_name, cfg_name, cfg_desc, mkfile_loc, build_opt, clean_opt, tool_id)
		if os.path.exists(cconf_xml_file) == True:
			cconf_xml_file_reader = open(cconf_xml_file, 'r').read()
			xml_fp.write(cconf_xml_file_reader)
			xml_fp.write('\r\n')
			os.remove(cconf_xml_file) ## delete it ##

	xml_fp.close()
	pass


def refreshscope_conf_nodes_gen(tmpl, xml, prj_name, **build_confs):
	'''
	'''
	if build_confs == None:
		return

	xml_fp = open(xml, 'w+') # #gnu/baremetal_arc_feature_cache/rsfs__baremetal_arc_feature_cache.xml
	xml_fp.seek(0)
	index = 0
	for build_conf in build_confs:
		cfg_name = build_conf
		rsf_xml_file = xml + 'conf_' + str(index)#gnu/baremetal_arc_feature_cache/rsfs__baremetal_arc_feature_cache.xmlconf_0
		index = index + 1
		# generate one refreshscope conf xml file,
		# read it and write it to all refreshscope conf file,
		# then delete the conf file #
		refreshscope_conf_node_gen(tmpl, rsf_xml_file, prj_name, cfg_name)#将./templates/gnu/refresh_configuration.tmpl内容用prj_name, cfg_name填充之后写入gnu/baremetal_arc_feature_cache/rsfs__baremetal_arc_feature_cache.xmlconf_0
		if os.path.exists(rsf_xml_file) == True:
			rsf_xml_file_reader = open(rsf_xml_file, 'r').read()
			xml_fp.write(rsf_xml_file_reader)#然后写进#gnu/baremetal_arc_feature_cache/rsfs__baremetal_arc_feature_cache.xml
			xml_fp.write('\r\n')
			os.remove(rsf_xml_file) ## delete it ##

	xml_fp.close()
	pass

def cproject_file_gen(tmpls, xml, prj_name, **build_confs):
	'''
	Generate cproject file using template file
	'''
#	print tmpls, xml, prj_name    tmpl #./templates/gnu/cproject.tmpl, ./templates/gnu/cconfiguration.tmpl, ./templates/gnu/refresh_configuration.tmpl, xml #gnu/baremetal_arc_feature_cache/.cproject
#	print build_confs conf clean命令之前的配置

	## get templates from tmpls ##
	#        0         		         1             		        2
	# cproject_template		cconfiguration_template		refreshscope_template
	##
	tmpls_list = tmpls.strip(' ').strip(',').split(',')# [./templates/gnu/cproject.tmpl, ./templates/gnu/cconfiguration.tmpl, ./templates/gnu/refresh_configuration.tmpl]
	cprj_tmpl = tmpls_list[0].strip() #./templates/gnu/cproject.tmpl,
	cconf_tmpl = tmpls_list[1].strip() # ./templates/gnu/cconfiguration.tmpl
	rsf_tmpl = tmpls_list[2].strip() #./templates/gnu/refresh_configuration.tmpl

	## get xml directory by xml file name ##
	xml_dir = os.path.dirname(xml)#gnu/baremetal_arc_feature_cache/.cproject
	cconfs_xml_file = str(xml_dir) + '/cconfs_' + str(prj_name) + '.xml' # gnu/baremetal_arc_feature_cache/cconfs_baremetal_arc_feature_cache.xml
	rsfs_xml_file = str(xml_dir) + '/rsfs_' + str(prj_name) + '.xml' # gnu/baremetal_arc_feature_cache/rsfs__baremetal_arc_feature_cache.xml

	#将./templates/gnu/cconfiguration.tmpl内的字符替换掉写进gnu/baremetal_arc_feature_cache/cconfs_baremetal_arc_feature_cache.xmlconf_0
	cconfiguration_nodes_gen(cconf_tmpl, cconfs_xml_file, prj_name, **build_confs)##./templates/gnu/cproject.tmpl, gnu/baremetal_arc_feature_cache/cconfs_baremetal_arc_feature_cache.xml
	refreshscope_conf_nodes_gen(rsf_tmpl, rsfs_xml_file, prj_name, **build_confs)##./templates/gnu/refresh_configuration.tmpl填充内容之后写进 gnu/baremetal_arc_feature_cache/rsfs__baremetal_arc_feature_cache.xml

	if os.path.exists(cconfs_xml_file) == True:
		cconf_xml_str = open(cconfs_xml_file, 'r').read().strip('\r\n')
		os.remove(cconfs_xml_file) ## delete it ##
	else:
		cconf_xml_str = ''

	if os.path.exists(rsfs_xml_file) == True:
		rsf_xml_str = open(rsfs_xml_file, 'r').read().strip('\r\n')
		os.remove(rsfs_xml_file) ## delete it ##
	else:
		rsf_xml_str = ''
	#读取生成的文件之后删除

	cprj_xml_fp = open(xml, 'w+') ##gnu/baremetal_arc_feature_cache/.cproject
	tmpl_reader = open(cprj_tmpl, 'r').read()##./templates/gnu/cproject.tmpl,

	TO_REPLACE_KEYS = ["$PRJ_NAME$", "$CCONFIG$", "$REFRESH_SCOPE_CONF$"]
	REPLACED_KEYS = [prj_name, cconf_xml_str, rsf_xml_str]

	i = 0
	for key in TO_REPLACE_KEYS:
		tmpl_reader = tmpl_reader.replace(str(key), str(REPLACED_KEYS[i])) # 将从中间文件读取的内容填充到./templates/gnu/cproject.tmpl然后写入gnu/baremetal_arc_feature_cache/.cproject
		i = i + 1

	cprj_xml_fp.seek(0)
	cprj_xml_fp.write(tmpl_reader)
	cprj_xml_fp.close()

	pass

def link_node_fill(parent, name, type, loc):
	## link node in linkedResources node ##
	link_node = ET.SubElement(parent, 'link')
	link_node.text = parent.text + '\t'
	link_node.tail = parent.text
	## name node in link node ##
	name_node = ET.SubElement(link_node, 'name')
	name_node.text = name
	name_node.tail = link_node.text
	## type node in link node ##
	type_node = ET.SubElement(link_node, 'type')
	type_node.text = type
	type_node.tail = link_node.text
	## locationURI node in link node ##
	loc_node = ET.SubElement(link_node, 'locationURI')
	loc_node.text = loc
	loc_node.tail = link_node.tail

	return link_node
	pass


def link_node_add(parent, link_folder):##[arc,board,device,inc,middleware,library,options,os,example/baremetal/arc_feature/cache]
	'''
	Add link node to parent node, when link folder is a folder with parent folder,
	create virtual parent folder for it
	'''
	## Strip ' ' and /' for link_folder ##
	link_folder = link_folder.strip()
	link_folder = link_folder.strip('/')
	## Get max depth need to create virtual folder (0 for no virtual folder create need)##
	virtual_folder_depth = len(link_folder.split('/')) - 1

	## add virtual node ##
	if virtual_folder_depth > 0:
		for i in range(virtual_folder_depth, 0, -1):
			node_name = link_folder.rsplit('/', i)[0]
			#print i, link_folder.rsplit('/', i)
			link_node_fill(parent, node_name, '2', "virtual:/virtual")

	return link_node_fill(parent, link_folder, '2', "SRCS_ROOT/"+link_folder)
	pass


def project_file_gen(tmpl, xml, prj_name, srcroot_depth, link_src_folders):#写gnu/baremetal_arc_feature_cache/.project，添加子节点
	'''
	Generate project file using template file
	'''
	prj_xml_fp = open(xml, 'w+') ##gnu/baremetal_arc_feature_cache/.project
	tmpl_reader = open(tmpl, 'r').read()#./templates/gnu/project.tmpl

	## Do template replacement ##
	TO_REPLACE_KEYS = ["$PRJ_NAME$", "$ROOT_DEPTH$"]
	REPLACED_KEYS = [prj_name, str(srcroot_depth)] #baremetal_arc_feature_cache

	i = 0
	for key in TO_REPLACE_KEYS: # 填充templ中的变量
		tmpl_reader = tmpl_reader.replace(str(key), str(REPLACED_KEYS[i]))
		i = i + 1

	prj_xml_fp.seek(0)#将./templates/gnu/project.tmpl 填充之后写入 gnu/baremetal_arc_feature_cache/.project
	prj_xml_fp.write(tmpl_reader)
	prj_xml_fp.close()

	## do xml add node ##
	prj_xml_et = ET.parse(xml)
	# find the node named linkedResources #
	links_node = prj_xml_et.find("linkedResources")

	if links_node == None:
		return

	link_src_folders = link_src_folders.strip() #arc,board,device,inc,middleware,library,options,os,example/baremetal/arc_feature/cache
	link_src_folders = link_src_folders.strip(',')
	link_folders = link_src_folders.split(',')#[arc,board,device,inc,middleware,library,options,os,example/baremetal/arc_feature/cache]

	links_node.text = links_node.text + '\t'

	for link_folder in link_folders:
		link_node = link_node_add(links_node, link_folder) #在gnu/baremetal_arc_feature_cache/.project的linkedResources加入多个link子节点

	## Fix the last link node ##
	if link_node != None:
		link_node.tail = links_node.tail

	prj_xml_et.write(xml, 'UTF-8', True)

	pass

def openocd_digilent_jtagusb_dbgconf_file_gen(tmpl, xml, prj_name, cfg_name, elf_path, opnocd_cfg, tool_id):#将./templates/gnu/openocd_digilent.launchtmpl内容填充之后写入gnu/baremetal_arc_feature_cache/baremetal_arc_feature_cache-core4.lanuch
	'''
	Generate debug configuration file for metaware ide using digilent usb-jtag
	'''
	global digilent_debug_server_port #digilent_debug_server_port = 49105
	global openocd_bin_path #"C:\\arc_gnu\\bin\openocd.exe"
	TO_REPLACE_KEYS = ["$PRJ_NAME$", "$CFG_NAME$", "$ELF_PATH$", "$OPENOCD_CFG_PATH$", "$TOOL_ID$", "$PORT_NUM$", "$OPENOCD_BIN_PATH$"]
	port_num = digilent_debug_server_port
	REPLACED_KEYS = [prj_name, cfg_name, elf_path, opnocd_cfg, tool_id, port_num, openocd_bin_path]

	xml_fp = open(xml, 'w+')
	tmpl_reader = open(tmpl, 'r').read()

	i = 0
	for key in TO_REPLACE_KEYS:
		tmpl_reader = tmpl_reader.replace(str(key), str(REPLACED_KEYS[i]))
		i = i + 1

	xml_fp.seek(0)
	xml_fp.write(tmpl_reader)
	xml_fp.close()
	pass

def openocd_digi_jtag_debug_confs_gen(tmpl, conf_dir, prj_name, **dbg_confs):
	if dbg_confs == None:
		return

	### debug conf_table ##
	## key_name :    0          1            2
	## cfg_name : elf_path   opnocd_cfg   tool_id
	#######################
	#print "openocd_digi_jtag_debug_confs_gen...................{}".format(dbg_confs)
	for dbg_conf in dbg_confs:
		cfg_name = dbg_conf #core name
		dbg_conf_table = dbg_confs[dbg_conf].split('<>')
		elf_path = dbg_conf_table[0].strip() # ./obj_emsk_11/gnu_arcem4/baremetal_arc_feature_cache_gnu_arcem4.elf
		opnocd_cfg = dbg_conf_table[1].strip()# C:\arc_gnu\share\openocd\scripts\board\snps_em_sk_v1.cfg
		tool_id  = dbg_conf_table[2].strip()# 随机生成数
		dbg_conf_xml = conf_dir.strip().strip('/') + '/' + prj_name + '-' + cfg_name + '.launch'#gnu/baremetal_arc_feature_cache/baremetal_arc_feature_cache-core4.lanuch
		openocd_digilent_jtagusb_dbgconf_file_gen(tmpl, dbg_conf_xml, prj_name, cfg_name, elf_path, opnocd_cfg, tool_id)

	pass

def gnuide_project_gen(prj_name, gnuide_prj_loc, tmpls, src_dirs, **confs):
	if os.path.exists(gnuide_prj_loc) == False:
		os.mkdir(gnuide_prj_loc)

	# './templates/gnu/project.tmpl, ./templates/gnu/cproject.tmpl, ./templates/gnu/cconfiguration.tmpl, ./templates/gnu/refresh_configuration.tmpl, ./templates/gnu/openocd_digilent.launchtmpl'
	tmpls_list = tmpls.split(',')
	# tmpls ---gen list--->  tmpls_list
	#     0                  1                  2                       3                   4
	# .project_tmpl   .cproject_tmpl    .cproject_cconf_tmpl    .cproject_rsf_tmpl    debug_conf_tmpl
	prj_tmpl = tmpls_list[0].strip()#./templates/gnu/project.tmpl
	cprj_tmpls = tmpls_list[1] + ',' + tmpls_list[2] + ',' + tmpls_list[3]#./templates/gnu/cproject.tmpl, ./templates/gnu/cconfiguration.tmpl, ./templates/gnu/refresh_configuration.tmpl,
	dbg_conf_tmpl = tmpls_list[4].strip(' ')#./templates/gnu/openocd_digilent.launchtmpl

	core_confs = confs.copy()
	dbg_confs = confs.copy()

	### conf_table ##
	## key_name :     0         1           2          3         4         5          6
	## cfg_name : cfg_desc, mkfile_loc, build_opt, clean_opt  elf_path  opnocd_cfg  tool_id
	#######################
	for conf in confs:
		conf_tbl = confs[conf].rsplit('<>', 3) #从尾部向前分割 [。。] /clean命令/ elf / gnu cfg
		## CONF TBL ##
		#     0           1          2         3
		# BUILD_CFG   ELF_PATH  OPNOCD_CFG  TOOL_ID
		core_confs[conf] = conf_tbl[0] + ' <> ' + conf_tbl[3] #[。。] / gnu cfg
		dbg_confs[conf]  = conf_tbl[1] + ' <> ' + conf_tbl[2] + ' <> ' + conf_tbl[3]#  elf / gnu cfg

	prj_gene_file = gnuide_prj_loc+'/.project' #gnu/baremetal_arc_feature_cache/.project
	prj_dir_depth = ide_workspace_relative_depth #3
	cprj_gene_file = gnuide_prj_loc+'/.cproject'#gnu/baremetal_arc_feature_cache/.cproject

	project_file_gen(prj_tmpl, prj_gene_file, prj_name, prj_dir_depth, src_dirs)
	cproject_file_gen(cprj_tmpls, cprj_gene_file, prj_name, **core_confs)
	openocd_digi_jtag_debug_confs_gen(dbg_conf_tmpl, gnuide_prj_loc, prj_name, **dbg_confs)#./templates/gnu/openocd_digilent.launchtmpl  gnu/baremetal_arc_feature_cache 
	#将./templates/gnu/openocd_digilent.launchtmpl内容填充之后写入gnu/baremetal_arc_feature_cache/baremetal_arc_feature_cache-core4.lanuch
	pass
##
# Project Description File Template #
# project_name := xxxx
# srcs_dir := xx,xx,xx,xx
# CONF_xx := xxx <> xxx <> xxx <> xxx <> xxx
# CONF_xx := xxx <> xxx <> xxx <> xxx <> xxx
# ++++++++++++++++++++++++
def prj_desc_parse(fp):
	prj_name = ''
	src_dirs = ''
	confs = dict()

	if fp == None:
		return False, prj_name, src_dirs, confs

	while True:
		newline = fp.readline()
		if newline == '':
			break
		newline = newline.strip()
		if newline == '':
			continue
		newline_list = newline.split(':=')

		if len(newline_list) < 2:
			break

		key = newline_list[0].strip()
		key_val = newline_list[1].strip()

		if cmp(key, 'project_name') == 0:
			prj_name = key_val
			continue

		if cmp(key, 'srcs_dir') == 0:
			src_dirs = key_val
			continue

		if key.startswith('CONF_') == True:
			confs[key[5:]] = key_val
			continue

	if prj_name != '' and src_dirs != '' and len(confs) > 0:
		# print prj_name
		# print src_dirs
		# print confs
		return True, prj_name, src_dirs, confs
	else:
		return False, prj_name, src_dirs, confs
	pass

def gnuide_projects_gen(prj_root_dir, tmpls, project_desc_file):# 读取 example_ide_project_desc.txt 填写.cproject .project 和 多个。lanuch文件
	prj_desc_filefp = open(project_desc_file, 'r')

	if prj_desc_filefp == None:
		return
	if os.path.exists(prj_root_dir) == False:
		os.mkdir(prj_root_dir)

	Go_on = True
	while Go_on:
		Go_on, prj_name, src_dirs, confs = prj_desc_parse(prj_desc_filefp)# 每次读取 example_ide_project_desc.txt一块
		if Go_on:
			gnuide_prj_loc = prj_root_dir.rstrip('/') + '/' + prj_name #gnu/baremetal_arc_feature_cache
			print 'Generate GNU IDE Project ' + prj_name + ' into ' + gnuide_prj_loc
			gnuide_project_gen(prj_name, gnuide_prj_loc, tmpls, src_dirs, **confs) #填写。cproject .project 和 多个。lanuch文件

	prj_desc_filefp.close()
	pass

def find_file_recursive(path, min_depth, max_depth, filename):
	path_matches = list()
	if os.path.exists(path) == False and min_depth > max_depth:
		return path_matches

	filename = filename.strip()

	for root, dirs, files in os.walk(path, False):
		# replace windows path to linux #
		root = root.replace('\\', '/')
		roottemp = root[len(path):].strip('/')
		if roottemp == '':
			find_depth_now = 0
		else:
			find_depth_now = len(roottemp.split('/'))
		#print find_depth_now, root, roottemp
		# break when reach max depth #
		if find_depth_now > max_depth:
			continue
		if find_depth_now >= min_depth:
			if filename in files:
				path_matches.append(roottemp)

	return path_matches
	pass
'''
def embARC_projects_desc_file_gen(tmpls, prj_path, ide_workloc):
	em_configs = {
		'arcem4'	: 'EM4 Configuration',
		'arcem6'	: 'EM6 Configuration',
		'arcem6gp'	: 'EM6 GP Configuration',
		'arcem5d'	: 'ARC EM5D Configuration',
		'arcem7d'	: 'ARC EM7D Configuration',
		'arcem7dfpu'	: 'ARC EM7D FPU Configuration'
	}
	common_src_dirs = 'arc,board,device,inc,middleware,options,os'
	## here must use \\b instead of \b'
	OPENOCD_CFG_PATH_GNUIDE = "C:\ARC\ARC_GNU_IDE_2014.08\share\openocd\scripts\\board\snps_em_sk.cfg"

	prj_path = prj_path.strip()
	ide_workloc = ide_workloc.strip()

	if prj_path == '' or ide_workloc == '':
		return

	examples_mk_path_1 = find_file_recursive(prj_path, 1, 6, 'Makefile')
	examples_mk_path_2 = find_file_recursive(prj_path, 1, 6, 'makefile')
	example_mk_path = examples_mk_path_1 + examples_mk_path_2

	if len(example_mk_path) == 0:
		return

	prj_desc_filename = prj_path.rstrip('/') + '/' + 'example_ide_project_desc.txt'
	prj_desc_filefp = open(prj_desc_filename, 'w+')

	for example in example_mk_path:
		example_path = os.path.basename(prj_path) + '/' + example
		prj_name = example.strip().replace('/', '_').replace(' ', '-')
		src_dirs = common_src_dirs + ',' + example_path
		confs = dict()
		prj_name_line = 'project_name := ' + prj_name + '\r\n'
		src_dirs_line = 'srcs_dir := ' + src_dirs + '\r\n'
		prj_desc_filefp.write(prj_name_line + src_dirs_line)
		for emconf in em_configs:
			conf = emconf.strip()
			appl_name = prj_name + '_gnu_' + conf
			obj_dir_root = '${ProjDirPath}'
			build_opt = 'CUR_CORE=' + conf + ' TOOLCHAIN=gnu ' + ' OUT_DIR_ROOT=' + obj_dir_root + ' APPL=' + prj_name + ' all'
			clean_opt = 'CUR_CORE=' + conf + ' TOOLCHAIN=gnu ' + ' OUT_DIR_ROOT=' + obj_dir_root + ' APPL=' + prj_name + ' clean'
			obj_dir = './' + 'obj' + '_gnu_' + conf
			elf_loc = obj_dir + '/' + appl_name + '.elf'
			opnocd_cfg = OPENOCD_CFG_PATH_GNUIDE
			# random a toolid (from 1000000000 to 2000000000) #
			tool_id = random.randint(1000000000, 2000000000)

			confs[conf] = em_configs[emconf] + ' <> ' + example_path + ' <> ' + build_opt + ' <> ' + clean_opt + ' <> ' + elf_loc  + ' <> ' + opnocd_cfg + ' <> ' + str(tool_id)
			conf_line = 'CONF_' + conf + ' := ' + confs[conf] + '\r\n'
			prj_desc_filefp.write(conf_line)

		prj_desc_filefp.write('++++++++++++++++++++++++\r\n')

	prj_desc_filefp.close()

	gnuide_projects_gen(ide_workloc, tmpls, prj_desc_filename)

	# Finally remove the project description file
	if os.path.exists(prj_desc_filename) == True:
		os.remove(prj_desc_filename)

	# print example_mk_path
	pass'''

def embARC_project_board_cfg_parse(fp):# Board Information下的配置转换成字典返回
	board_cfgs = dict()
	board_cfg_tag = "Board Information"

	if fp == None:
		return False, board_cfgs

	# find board_cfg_tag
	while True:
		newline = fp.readline()
		if newline == '':
			return False, board_cfgs

		newline = newline.strip()
		if newline == '':
			continue

		newline = newline.strip('+')

		if cmp(newline, board_cfg_tag) == 0:
			break

	# then the following is build configurations
	while True:
		newline = fp.readline()
		if newline == '':
			break

		newline = newline.strip()
		if newline == '':
			continue

		# Check if it is a next block #
		if newline.startswith('++') == True:
			break

		# find configuration, split using : , cfg:cfg_desc #
		newline_list = newline.split(':')
		if len(newline_list) < 2:
			continue

		# strip blank tab crlf #
		board_cfg = newline_list[0].strip()
		board_cfg_desc = newline_list[1].strip()
		# add it to a dict
		board_cfgs[board_cfg] = board_cfg_desc

	# Finish Parse #
	return True, board_cfgs

	pass

def embARC_project_build_cfg_parse(fp):
	build_cfgs = dict()
	build_cfg_tag = "Configuration Information"

	if fp == None:
		return False, build_cfgs

	# find build_cfg_tag
	while True:
		newline = fp.readline()
		if newline == '':
			return False, build_cfgs

		newline = newline.strip()
		if newline == '':
			continue

		newline = newline.strip('+')
		if cmp(newline, build_cfg_tag) == 0:
			break

	# then the following is build configurations
	while True:
		newline = fp.readline()
		if newline == '':
			break

		newline = newline.strip()
		if newline == '':
			continue

		# Check if it is a next block #
		if newline.startswith('++') == True:
			break

		# find configuration, split using : , cfg:cfg_desc #
		newline_list = newline.split(':')
		if len(newline_list) < 2:
			continue

		# strip blank tab crlf #
		build_cfg = newline_list[0].strip()
		build_cfg_desc = newline_list[1].strip()
		# add it to a dict
		build_cfgs[build_cfg] = build_cfg_desc

	# Finish Parse #
	return True, build_cfgs

	pass

def embARC_project_cfg_names_parse(fp):
	project_cfg_names = list()
	project_cfg_tag = "Analysis Report"

	if fp == None:
		return False, project_cfg_names

	# find project_cfg_tag
	while True:
		newline = fp.readline()
		if newline == '':
			return False, project_cfg_names

		newline = newline.strip()
		if newline == '':
			continue

		newline = newline.strip('+')
		if cmp(newline, project_cfg_tag) == 0:
			break

	# then the following is build configurations
	result = False
	while True:
		newline = fp.readline()
		if newline == '':
			break

		newline = newline.strip()
		if newline == '':
			continue

		# Check if it is a next block #
		if newline.startswith('++') == True:
			break

		# find project configuration name line, split using TAB #
		# prj_name	prj_path	srcs_folders	core_cfg0	... 	core_cfgn #
		newline_list = newline.split('\t')

		for key in newline_list:
			key = key.strip()
			if key != '':
				# add new key #
				project_cfg_names.append(key)

		# break when parse this line #
		result = True
		break

	# Finish Parse #
	return result, project_cfg_names

	pass

def embARC_project_cfg_read(fp, *project_cfg_names):
	project_cfg = dict()

	if fp == None:
		return False, project_cfg

	result = False
	while True:
		newline = fp.readline()
		if newline == '':
			break

		newline = newline.strip()
		if newline == '':
			continue

		# Check if it is a next block #
		if newline.startswith('++') == True:
			break

		# find project configuration line, split using TAB #
		# prj_name	prj_path	srcs_folders	core_cfg0	... 	core_cfgn #
		newline_list = newline.split('\t')

		count = 0
		length = len(project_cfg_names)
		for cfg in newline_list:
			cfg = cfg.strip()
			if cfg != '' and count < length:
				project_cfg[project_cfg_names[count]] = cfg
				count = count + 1

		# break when parse this line #
		result = True
		break

	return result, project_cfg

	pass

def embARC_projects_gen(tmpls, prj_status_file, ide_workloc, openocd_loc):
	'''
	Generate GNU IDE Project FIles using generated examples compiling status file
	'''
	CONF_NOT_EXIST_TAG='xx'
	default_board='emsk'
	default_bd_ver='11'
	toolchain='gnu'
	openocd_loc = openocd_loc.strip().replace('/', '\\')
	OPENOCD_CFG_PATH_GNUIDE = openocd_loc
	print "........................."
	print OPENOCD_CFG_PATH_GNUIDE
	prj_status_file = prj_status_file.strip()
	ide_workloc = ide_workloc.strip()

	if prj_status_file == '' or ide_workloc == '':
		return False

	# check if the project build status file exists
	if os.path.exists(prj_status_file) == False:
		return False

	fp = open(prj_status_file, 'r')

	# get board configuration name and its descriptions #
	result, board_cfg = embARC_project_board_cfg_parse(fp) # Board Information下的配置转换成字典返回
	if result == False:
		board=default_board
		bd_ver=default_bd_ver
	else:
		board=board_cfg['board']
		bd_ver=board_cfg['board_version']

	fp.seek(0)
	# get build configuration name and its descriptions #
	result, build_cfgs = embARC_project_build_cfg_parse(fp)# Configuration Information下的配置字典core
	if result == False:
		fp.close()
		return False

	fp.seek(0)
	result, project_cfg_names = embARC_project_cfg_names_parse(fp)#Analysis Report下一行表头信息
	if result == False:
		fp.close()
		return False

	# check if the ide workspace exists
	if os.path.exists(ide_workloc) == False:# gnu文件夹
		os.mkdir(ide_workloc)
	prj_desc_filename = ide_workloc.rstrip('/') + '/' + 'example_ide_project_desc.txt'
	prj_desc_filefp = open(prj_desc_filename, 'w+')#gnu/example_ide_project_desc.txt
	while True:
		result, project_cfg = embARC_project_cfg_read(fp, *project_cfg_names)#每次读取一行Analysis Report下面面的信息，返回一个字典
		if result == False:
			break
		prj_name = project_cfg['prj_name'].strip()
		example_path = project_cfg['example_path'].strip().replace('\\', '/')
		src_dirs = project_cfg['src_dirs'] + ',' + example_path
		confs = dict()
		prj_name_line = 'project_name := ' + prj_name + '\r\n'
		src_dirs_line = 'srcs_dir := ' + src_dirs + '\r\n'
		# set to nothing #
		cfgs_line = ''
		for emconf in build_cfgs:#字典，key是arcem4  arcem4 arcem6gp，对于每个core获取olevel信息
			conf = emconf.strip()
			appl_name = prj_name + '_' + toolchain + '_' + conf #baremetal_arc_feature_cache_gni_arcem4  baremetal_arc_feature_cache_gni_arcem6 ,,,,,
			obj_dir_root = '${ProjDirPath}'
			# check if key exists in project cfg dict #
			if project_cfg.has_key(conf) == False:
				# continue next build configuration if conf not exists
				continue
			olevels = project_cfg[conf].strip()
			# check if this configuration is valid, if not valid then don't add to configurations #
			if olevels.startswith(CONF_NOT_EXIST_TAG) == True:
				continue
			olevel_list = olevels.replace(' ', '').split(',')
			if len(olevel_list) == 0:
				continue
			# select a optimization level from that valid ones #
			# select the last one, because it is the best optimized #
			olevel = olevel_list[len(olevel_list)-1]#选择最后一个olevel
			print 'Select optimization level ' + olevel + ' from ' + str(olevel_list) + ' for ' + appl_name

			# build_opt = 'BOARD=' + board + ' BD_VER=' + bd_ver + ' CUR_CORE=' + conf + ' TOOLCHAIN=' + toolchain + ' OUT_DIR_ROOT=' + obj_dir_root + ' APPL=' + prj_name + ' OLEVEL=' + olevel + ' all'
			# clean_opt = 'BOARD=' + board + ' BD_VER=' + bd_ver + ' CUR_CORE=' + conf + ' TOOLCHAIN=' + toolchain + ' OUT_DIR_ROOT=' + obj_dir_root + ' APPL=' + prj_name + ' OLEVEL=' + olevel + ' clean'
			build_opt = 'BOARD=' + board + ' BD_VER=' + bd_ver + ' CUR_CORE=' + conf + ' TOOLCHAIN=' + toolchain + ' OUT_DIR_ROOT=' + obj_dir_root + ' APPL=' + prj_name + ' all'
			clean_opt = 'BOARD=' + board + ' BD_VER=' + bd_ver + ' CUR_CORE=' + conf + ' TOOLCHAIN=' + toolchain + ' OUT_DIR_ROOT=' + obj_dir_root + ' APPL=' + prj_name + ' clean'
			board_info = board + '_' + bd_ver
			build_info = toolchain + '_' + conf
			if new_obj_folder_gen == 1: #全局 1
				obj_dir = './' + 'obj_' + board_info + '/' + build_info # ./obj_emsk_11/gnu_arcem4
			else:
				obj_dir = './' + 'obj_' + build_info

			elf_loc = obj_dir + '/' + appl_name + '.elf' # ./obj_emsk_11/gnu_arcem4/baremetal_arc_feature_cache_gni_arcem4.elf
			opnocd_cfg = OPENOCD_CFG_PATH_GNUIDE
			# random a toolid (from 1000000000 to 2000000000) #
			tool_id = random.randint(1000000000, 2000000000)

			confs[conf] = build_cfgs[emconf] + ' <> ' + example_path + ' <> ' + build_opt + ' <> ' + clean_opt + ' <> ' + elf_loc  + ' <> ' + opnocd_cfg + ' <> ' + str(tool_id)
			conf_line = 'CONF_' + conf + ' := ' + confs[conf] + '\r\n'
			cfgs_line += conf_line

		# has configuration in it, then write new project description #
		if cfgs_line != '': #gnu/example_ide_project_desc.txt写入
			prj_desc_filefp.write(prj_name_line + src_dirs_line) # project_name := baremetal_arc_feature_cache\r\n + srcs_dir := arc,board,device,inc,middleware,library,options,os,example/baremetal/arc_feature/cache
			prj_desc_filefp.write(cfgs_line)
			prj_desc_filefp.write('++++++++++++++++++++++++\r\n')

	fp.close()
	prj_desc_filefp.close()
	dst= "test_example_ide_project_desc.txt"
	shutil.copyfile(prj_desc_filename, dst)

	gnuide_projects_gen(ide_workloc, tmpls, prj_desc_filename) # tmpls = GNUIDE_PRJ_TMPLS # 读取 example_ide_project_desc.txt 填写.cproject .project 和 多个。lanuch文件

	# Finally remove the project description file
	if os.path.exists(prj_desc_filename) == True:
		os.remove(prj_desc_filename)

	return True
	pass

GNUIDE_PRJ_TMPLS = './templates/gnu/project.tmpl, ./templates/gnu/cproject.tmpl, ./templates/gnu/cconfiguration.tmpl, ./templates/gnu/refresh_configuration.tmpl, ./templates/gnu/openocd_digilent.launchtmpl'

def usage():
	print "-h, -H, -?, --help			Print Usage of IDE Generator"
	print "-w WORKSPACE_LOC, --workspace=WORKSPACE_LOC "
	print "						Set where to generate the IDE workspace"
	print "-s PROJECT_STATUS_FILE, --status=PROJECT_STATUS_FILE "
	print "						Set the project status file needed by generator"
	print "-c OPENOCD_CFG, --cfg=OPENOCD_CFG "
	print "						Set the openocd cfg file location needed by generator"
	print "-d WORKSPACE_DEPTH, --depth=WORKSPACE_DEPTH "
	print "						Set the ide workspace relative depth needed by generator"
	print "-p OPENOCD_PORT, --port=OPENOCD_PORT "
	print "						Set the openocd debugger server port needed by generator"
	print "-o OPENOCD_BIN_LOC, --openocd=OPENOCD_BIN_LOC "
	print "						Set openocd binary file location needed by generator"
	print "-b DEFAULT_BUILD_CONF --build=DEFAULT_BUILD_CONF"
	print "						Set default build configuration"

def main():
	global ide_workspace_relative_depth, digilent_debug_server_port, openocd_bin_path, default_build_conf

	try:
		opts, args = getopt.getopt(sys.argv[1:], 'w:s:c:d:p:o:b:hH?', ["help", "workspace=", "status=", "cfg=", "depth=", "port=", "openocd=", "build="])
	except getopt.GetoptError as err:
		print str(err)
		usage()
		sys.exit(2)

	workspace_loc='gnu'
	prj_status_file='./build_report/emsk_11/gnu_analysis_report.txt'
	openocd_loc = "C:\\arc_gnu\share\openocd\scripts\\board\snps_em_sk_v1.cfg"
	depth = 2
	port_num = digilent_debug_server_port
	for arg, opt in opts:
		if arg in ("-h", "-H", "-?", "--help"):
			usage()
			sys.exit(2)
		elif arg in ("-w", "--workspace"):
			workspace_loc = opt.strip()
		elif arg in ("-s", "--status"):
			prj_status_file = opt.strip()
		elif arg in ("-c", "--cfg"):
			openocd_loc = opt.strip()
		elif arg in ("-d", "--depth"):
			try:
				depth = int(opt.strip())
			except:
				depth = ide_workspace_relative_depth
			ide_workspace_relative_depth = depth
		elif arg in ("-p", "--port"):
			try:
				port_num = int(opt.strip())
			except:
				port_num = digilent_debug_server_port
			digilent_debug_server_port = port_num
		elif arg in ("-o", "--openocd"):
			openocd_bin_path = opt.strip()
		elif arg in ("-b", "--build"):
			default_build_conf = opt.strip()
		else:
			print "Unhandled Option"

	# Run Generator #
	print "Generate GNU IDE Projects in "  + "< " + workspace_loc  + " >" +  \
	" using project status file " + "< " + prj_status_file + " > ."
	print "Openocd Configuration file location is : " + openocd_loc
	print "Workspace relative depth is " + str(ide_workspace_relative_depth)
	print "Openocd Configuration file location is : " + openocd_loc
	print "Openocd Binary file location is " + openocd_bin_path
	print "Openocd Debugger Server Port  is : " + str(digilent_debug_server_port)

	status = embARC_projects_gen(GNUIDE_PRJ_TMPLS, prj_status_file, workspace_loc, openocd_loc)
	if status == False:
		print "IDE Generator Run Failed"

## Main Entry ##
if __name__ == '__main__':
	main()