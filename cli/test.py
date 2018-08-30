from __future__ import print_function, division
import unittest
from tools.template import template
from fixture import Destructing
from tools.download_manager import delete_dir_files
from fixture import Destructing
from tools.toolchain import arcToolchain, gnu, metaware

class TestTemplate(Destructing):
	def setUp(self):
		super(TestTemplate, self).setUp()
		self.config = {"appl": "testappl", "olevel":"O2", "board":"emsk", "bd_ver":"11", "cur_core":"arcem4", "toolchian":"gnu", "osp_root":"."}
	def test_render_makefile(self):
		result = template.render_makefile(self.config)
		self.assertTrue(result)
	def tearDown(self):
		pass
		#delete_dir_files("makefile")
		#self._del_to_be_sure("config")

class TestToolchain(Destructing):
	def setUp(self):
		super(TestToolchain, self).setUp()
		self.gnu = gnu.Gnu()
		self.mw = metaware.Mw()

	def test_is_support(self):
		result = arcToolchain.is_supported("gnu")
		self.assertTrue(result)
		result = arcToolchain.is_supported("mw")
		self.assertTrue(result)

	def test_get_platform(self):
		result = arcToolchain.get_platform()
		self.assertEqual(result, "Windows")

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

	def tearDown(self):
		pass

		#delete_dir_files("makefile")
		#self._del_to_be_sure("gnu")
		#self._del_to_be_sure("mw")

if __name__=='__main__':
	suit1 = unittest.TestLoader().loadTestsFromTestCase(TestTemplate)
	suit2 = unittest.TestLoader().loadTestsFromTestCase(TestToolchain)
	suite = unittest.TestSuite([suit1, suit2])
	unittest.TextTestRunner(verbosity=2).run(suite)
	#all_cases = unittest.defaultTestLoader.discover('.','test_*.py')
	'''suite = unittest.TestSuite()

	suite.addTest(unittest.makeSuite(TestToolchain))
	runner=unittest.TextTestRunner()
	runner.run(suite)'''

