from __future__ import print_function, division
from embarc_tools.osp import *
import unittest
import os, shutil
from embarc_tools.download_manager import getcwd
'''class TestGit(unittest.TestCase):
    def setUp(self):
        self.repourl = "https://github.com/wangnuannuan/embarc_emsk_bsp.git"
        self.path = os.path.join(getcwd(), "embarc_emsk_bsp")

    def test_formaturl(self):
        url1 = "https://github.com/foss-for-synopsys-dwc-arc-processors/embarc_osp.git"
        formurl1 = formaturl(url1)
        print(formurl1)
        url2 = "git@github.com:foss-for-synopsys-dwc-arc-processors/embarc_osp.git"
        formurl2 = formaturl(url2)
        print(formurl2)

    def test_git_command1(self):
        Git.init()
        Git.clone(self.repourl, self.path)
        Git.cleanup()



    def tearDown(self):
        Git.remove("embarc_emsk_bsp")
        pass
        #shutil.rmtree("embarc_emsk_bsp")'''
