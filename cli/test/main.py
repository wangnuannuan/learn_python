import unittest
from unittest import defaultTestLoader
import HTMLTestRunner
import coverage
import os
case_path = "."

def get_allcase():
    discover = unittest.defaultTestLoader.discover(case_path, pattern="test*.py")
    # suite = unittest.TestSuite()
    #suite.addTest(discover)
    #return suite
    return discover

if __name__ == '__main__':
    COV = coverage.coverage(branch=True, include='./embarc_tools/*')
    COV.start()
    testfilepath = "test.html"
    ftp = open(testfilepath,'wb')
    # runner = unittest.TextTestRunner()
    runner = HTMLTestRunner.HTMLTestRunner(stream=ftp, title="test result")
    runner.run(get_allcase())
    ftp.close()
    COV.stop()
    COV.save()
    print('Coverage Summary:')
    COV.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    COV.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)
    COV.erase()
