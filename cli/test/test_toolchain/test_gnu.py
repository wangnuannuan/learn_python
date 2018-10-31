from __future__ import print_function, division
from embarc_tools.toolchain import gnu, metaware, arcToolchain
import unittest
import os, shutil

class TestToolchain(unittest.TestCase):
    def setUp(self):
        super(TestToolchain, self).setUp()
        self.gnu = gnu.Gnu()
        self.mw = metaware.Mw()
        self.pack = "arc_gnu_2018.03_prebuilt_elf32_le_linux_install.tar.gz"

    def test_is_support(self):
        result = arcToolchain.is_supported("gnu")
        self.assertTrue(result)
        result = arcToolchain.is_supported("mw")
        self.assertTrue(result)

    def test_get_platform(self):
        result = arcToolchain.get_platform()
        self.assertIn(result, ["Windows", "Linux"])

    def test_check_version(self):
        gnuversion = self.gnu.check_version()
        print(gnuversion)
        mwversion = self.mw.check_version()
        print(mwversion)

    def test_download(self):
        gnu_tgz_path = self.gnu.download(version="2018.03")
        print("download ",gnu_tgz_path)

        self.assertIsNotNone(gnu_tgz_path)

    def test_extract_file(self):
        pack = "arc_gnu_2018.03_prebuilt_elf32_le_linux_install.tar.gz"
        path = self.gnu.extract_file(pack)
        print("gnu pack path: ",path)

    def test_set_toolchain_env(self):
        pass
        # self.gnu.set_toolchain_env("")

    def tearDown(self):
        if os.path.exists(self.pack):

            os.remove(self.pack)
        if os.path.exists("2018.03"):
            shutil.rmtree("2018.03")


