from __future__ import print_function, division
from embarc_tools.project import *
from embarc_tools.utils import uniqify
import unittest
import os
from embarc_tools.download_manager import cd

class TestIde(unittest.TestCase):
    def setUp(self):
        self.app_path = "C:\\Users\\jingru\\Documents\\embarc_tool\\embarc_tool\\test\\testapp"
        self.ide = Ide(path=self.app_path)


    def test__dict_elim_none(self):
        dict_test = {"a":[1, 2, 3, 4, 5, 5], "b": [1, 2, 1, 3, 1]}
        out_dic = self.ide._dict_elim_none(dict_test)
        print(out_dic)

    def test_get_project_conf_template(self):
        with cd(self.app_path):
            cproject_template = self.ide._get_project_conf_template()
            self.assertIsInstance(cproject_template["core"], dict)
            self.assertEqual(len(cproject_template["core"].keys()), 1)
            self.assertIsInstance(cproject_template["includes"], list)
            print(cproject_template["includes"]) 
            self.assertIn("testapp", cproject_template["includes"])

    def test_set_link_folders(self):
        includes = []
        link_folders, link_files, current_virtual_folders = self.ide.set_link_folders(includes)
        print(link_folders)
        self.assertIn("inc", link_folders)
        self.assertEqual(link_files, [])
        self.assertEqual(uniqify(current_virtual_folders), ["embARC"])

    def test_list_elim_none(self):
        test_list = [1, 2, 3, 4, 1]
        out_list = self.ide._list_elim_none(test_list)
        self.assertEqual(out_list, [1, 2, 3, 4, 1])

    def test_generate(self):
        self.ide.generate()
        file1 = ".project"
        file2 = ".cproject"
        self.assertTrue(os.path.exists(os.path.join(self.app_path, file1)))
        self.assertTrue(os.path.exists(os.path.join(self.app_path,file2)))

    def tearDown(self):
        file1 = ".project"
        file2 = ".cproject"
        if os.path.exists(os.path.join(self.app_path, file1)):
            os.remove(os.path.join(self.app_path, file1))
        if os.path.exists(os.path.join(self.app_path,file2)):
            os.remove(os.path.join(self.app_path,file2))
        pass
