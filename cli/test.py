from __future__ import print_function, division
import unittest
import HTMLTestRunner
from tools.template import template
from fixture import Destructing
from tools.download_manager import delete_dir_files,cd
from fixture import Destructing
from tools.toolchain import arcToolchain, gnu, metaware
import coverage
import os
from tools.builder import build
from tools.osp import (Git, formaturl, repo)

class TestTemplate(unittest.TestCase):
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


class TestToolchain(unittest.TestCase):
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

class TestBuilder(unittest.TestCase):
	def setUp(self):
		super(TestBuilder, self).setUp()
		self.app_path = "C:/Users/jingru/Documents/embarc_application/github/embarc_osp/example/baremetal/arc_feature/cache"
		self.osp_root = "C:/Users/jingru/Documents/embarc_application/github/embarc_osp"
		self.buildopts = {"BOARD":"emsk", "BD_VER":"11","CUR_CORE":"arcem6","TOOLCHAIN":"gnu"}
		
	def test_init(self):
		self.app_builder = build.embARC_Builder(osproot=self.osp_root, buildopts=self.buildopts, outdir='cur')

	def test_build_common_check(self):
		app_realpath, build_status = build.embARC_Builder().build_common_check(self.app_path)
		self.assertTrue(build_status["result"])

	def test_build_target(self):
		app_builder = build.embARC_Builder(osproot=self.osp_root, buildopts=self.buildopts, outdir='cur')
		build_status = app_builder.build_target(self.app_path, target='size')
		self.assertTrue(build_status["result"])

	def test_get_build_info(self):
		app_builder = build.embARC_Builder(osproot=self.osp_root, buildopts=self.buildopts, outdir='cur')
		print(app_builder.get_build_info(self.app_path))

	def test_build_elf(self):
		app_builder = build.embARC_Builder(osproot=self.osp_root, buildopts=self.buildopts, outdir='cur')
		build_status = app_builder.build_elf(self.app_path, pre_clean=True, post_clean=True)
		print(build_status['build_cmd'])
		print(build_status['time_cost'])
		print(build_status['build_msg'])
		self.assertTrue(build_status["result"])
		app_builder.distclean(self.app_path)

	def test_build_bin_hex(self):
		app_builder = build.embARC_Builder(osproot=self.osp_root, buildopts=self.buildopts, outdir='cur')
		build_status = app_builder.build_bin(self.app_path, pre_clean=True, post_clean=True)
		print(build_status['build_cmd'])
		print(build_status['time_cost'])
		print(build_status['build_msg'])
		self.assertTrue(build_status["result"])
		build_status = app_builder.build_hex(self.app_path, pre_clean=True, post_clean=True)
		print(build_status['build_cmd'])
		print(build_status['time_cost'])
		print(build_status['build_msg'])
		self.assertTrue(build_status["result"])
		app_builder.distclean(self.app_path)
	
	def test_get_build_size(self):
		app_builder = build.embARC_Builder(osproot=self.osp_root, buildopts=self.buildopts, outdir='cur')
		build_status = app_builder.get_build_size(self.app_path)
		print(build_status['build_cmd'])
		print(build_status['time_cost'])
		print(build_status['build_msg'])
		print(build_status['build_size'])
		self.assertTrue(build_status["result"])
		app_builder.distclean(self.app_path)

	def test_build_target_coverity(self):
		app_builder = build.embARC_Builder(osproot=self.osp_root, buildopts=self.buildopts, outdir='cur')
		build_status = app_builder.build_target(self.app_path,target='size',coverity=True)
		app_builder.build_coverity_result()
		self.assertTrue(build_status["result"])
		app_builder.distclean(self.app_path)

	def tearDown(self):
		print("test builder")


class TestOSP(unittest.TestCase):
	def setUp(self):
		self.repourl = "https://github.com/wangnuannuan/embarc_emsk_bsp.git"

	def test_formaturl(self):
		url1 = "https://github.com/foss-for-synopsys-dwc-arc-processors/embarc_osp.git"
		formurl1 = formaturl(formurl1)
		print(formurl1)
		url2 = "git@github.com:foss-for-synopsys-dwc-arc-processors/embarc_osp.git"
		formurl2 = formaturl(url2)
		print(formurl2)

	def test_git_command1(self):
		Git.init()
		Git.clone(self.repourl)
		Git.add(".")
		Git.remove("embarc_emsk_bsp")
		Git.cleanup()
	def test_git_command2(self):
		Git.clone(self.repourl)
		cd("embarc_emsk_bsp")
		Git.add(".")
		print(Git.getbranch())
		Git.commit("just test")
		Git.publish()
		Git.fetch()
		Git.checkout("master")
		Git.discard()
		Git.status()
		Git.dirty()
		Git.untracked()
	def tearDown(self):
		print("test osp")

if __name__=='__main__':
	COV = coverage.coverage(branch=True, include='tools/*')
	COV.start()
	testfilepath = "test.html"
	ftp=open(testfilepath,'wb')
	suit1 = unittest.TestLoader().loadTestsFromTestCase(TestTemplate)
	suit2 = unittest.TestLoader().loadTestsFromTestCase(TestToolchain)
	suit3 = unittest.TestLoader().loadTestsFromTestCase(TestBuilder)
	suit4 = unittest.TestLoader().loadTestsFromTestCase(TestOSP)
	suite = unittest.TestSuite([suit1, suit2, suit3])
	runner = HTMLTestRunner.HTMLTestRunner(stream=ftp,title="test result report")
	#unittest.TextTestRunner(verbosity=2).run(suite)
	runner.run(suite)
	ftp.close()
	COV.stop()
	COV.save()
	print('Coverage Summary:')
	COV.report()
	basedir = os.path.abspath(os.path.dirname(__file__))
	covdir = os.path.join(basedir, 'tmp/coverage')
	COV.html_report(directory=covdir)
	print('HTML version: file://%s/index.html' % covdir)
	COV.erase()
	#all_cases = unittest.defaultTestLoader.discover('.','test_*.py')
	'''suite = unittest.TestSuite()

	suite.addTest(unittest.makeSuite(TestToolchain))
	runner=unittest.TextTestRunner()
	runner.run(suite)'''

