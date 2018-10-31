from __future__ import print_function, division
from embarc_tools.notify import *
import unittest
import os

class TestNotify(unittest.TestCase):

    def setUp(self):
        self.notifier = TerminalNotifier()

    def test_collect_message(self):
        self.notifier.collect_message("hello")
        assert self.notifier.messages == ["[embARC] hello\n"]

    def test_notify(self):
        event = {
            "type": "info",
            "format": "string",
            "message": ""
        }
        result = self.notifier.notify(event)
        self.assertTrue(result)
        event["type"] = "None"
        result = self.notifier.notify(event)
        self.assertTrue(result)

    def tearDown(self):
        print("test builder")
