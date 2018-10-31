from __future__ import print_function, division
from embarc_tools.osp import repo, osp
import unittest
import os, shutil
from embarc_tools.download_manager import getcwd, rmtree_readonly

class TestRepo(unittest.TestCase):

    def setUp(self):
        self.repourl = "https://github.com/wangnuannuan/embarc_emsk_bsp.git"
        self.path = os.path.join(getcwd(), "embarc_emsk_bsp")

    def test_formaturl(self):
        osprepo = repo.Repo.fromurl(self.repourl)
        path = os.getcwd()
        if os.path.exists(self.path):
            rmtree_readonly("embarc_emsk_bsp")
        osprepo.clone(osprepo.url, path=os.path.join(path, osprepo.name), rev=None, depth=None, protocol=None, offline=False)

    def tearDown(self):
        try:
            rmtree_readonly("embarc_emsk_bsp")
        except Exception as e:
            pass


class TestOSP(unittest.TestCase):

    def setUp(self):

        self.osp_root = "C:/Users/jingru/Documents/embarc_application/embarc_osp"
        self.osppath = osp.OSP()

    def test_set_path(self):

        self.assertIsNone(self.osppath.set_path(self.osp_root))

    def test_get_path(self):
        result = self.osppath.get_path()
        self.assertEqual(result, self.osp_root)

    def test_is_osp(self):
        path = "path5"
        result = self.osppath.is_osp(path)
        self.assertFalse(result)

    def test_support_board(self):
        result = self.osppath.support_board(self.osp_root)
        self.assertIn("emsk", result)

    def test_get_board_version(self):
        result = self.osppath.get_board_version(self.osp_root, "emsk")
        self.assertIn("11", result)

    def test_get_tcfs(self):

        result = self.osppath.get_tcfs(self.osp_root, "emsk", "11")
        self.assertIn("arcem4", result)

    def test_get_makefile(self):
        osp_root, update = self.osppath.check_osp(self.osp_root)
        self.assertEqual(osp_root, self.osp_root.replace("\\", "/"))
        self.assertFalse(update)

    def test_get_makefile_config(self):
        build_template = dict()
        get_makefile = self.osppath.get_makefile(os.getcwd())
        makefile,result = self.osppath.get_makefile_config(build_template)
        if get_makefile:

            assert len(result) > 0
        else:

            self.assertEqual(result, build_template)







