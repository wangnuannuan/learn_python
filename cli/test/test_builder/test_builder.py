from __future__ import print_function, division
from embarc_tools.builder import build
import unittest
import os, shutil

class TestBuilder(unittest.TestCase):
    def setUp(self):
        super(TestBuilder, self).setUp()
        self.app_path = "C:\\Users\\jingru\\Documents\\embarc_tool\\embarc_tool\\test\\testapp"
        self.osp_root = "C:\\Users\\jingru\\Documents\\embarc_application\\embarc_osp"
        self.buildopts = {"BOARD":"emsk", "BD_VER":"11","CUR_CORE":"arcem6","TOOLCHAIN":"gnu"}
        self.app_builder = build.embARC_Builder(osproot=self.osp_root, buildopts=self.buildopts)

    def test_build_common_check(self):
        app_path = "C:\\Users\\jingru\\Documents\\embarc_tool\\embarc_tool\\test\\testapp"
        app_realpath, build_status = self.app_builder.build_common_check(app_path)
        self.assertTrue(build_status["result"])

    def test_build_target(self):
        app_path = "C:\\Users\\jingru\\Documents\\embarc_tool\\embarc_tool\\test\\testapp"
        build_status = self.app_builder.build_target(app_path, target='size')
        self.assertTrue(build_status["result"])

    def test_get_build_info(self):
        app_path = "C:\\Users\\jingru\\Documents\\embarc_tool\\embarc_tool\\test\\testapp"
        print(self.app_builder.get_build_info(app_path))

    def test_build_elf(self):
        app_path = "C:\\Users\\jingru\\Documents\\embarc_tool\\embarc_tool\\test\\testapp"
        build_status = self.app_builder.build_elf(app_path, pre_clean=False, post_clean=False)
        print(build_status['build_cmd'])
        print(build_status['time_cost'])
        print(build_status['build_msg'])
        self.assertTrue(build_status["result"])
        self.app_builder.distclean(self.app_path)

    def test_build_bin_hex(self):
        app_path = "C:\\Users\\jingru\\Documents\\embarc_tool\\embarc_tool\\test\\testapp"
        build_status = self.app_builder.build_bin(app_path, pre_clean=False, post_clean=False)
        print(build_status['build_cmd'])
        print(build_status['time_cost'])
        print(build_status['build_msg'])
        self.assertTrue(build_status["result"])
        build_status = self.app_builder.build_hex(app_path, pre_clean=False, post_clean=False)
        print(build_status['build_cmd'])
        print(build_status['time_cost'])
        print(build_status['build_msg'])
        self.assertTrue(build_status["result"])
        self.app_builder.distclean(self.app_path)

    def test_get_build_size(self):
        app_path = "C:\\Users\\jingru\\Documents\\embarc_tool\\embarc_tool\\test\\testapp"
        build_status = self.app_builder.get_build_size(app_path)
        print(build_status['build_cmd'])
        print(build_status['time_cost'])
        print(build_status['build_msg'])
        print(build_status['build_size'])
        self.assertTrue(build_status["result"])
        self.app_builder.distclean(self.app_path)
        

    
    '''def test_build_target_coverity(self):
        app_path = "C:\\Users\\jingru\\Documents\\embarc_tool\\embarc_tool\\test\\testapp"
        build_status = self.app_builder.build_target(app_path,target='all',coverity=True)
        self.app_builder.build_coverity_result()
        self.assertTrue(build_status["result"])
        app_builder.distclean(self.app_path)'''
        

    def tearDown(self):
        print("test builder")
