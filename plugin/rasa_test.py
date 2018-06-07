import rasa
import os
import unittest
from errbot.backends.test import testbot
from errbot import plugin_manager

class TestRasa(object):
    extra_plugin_dir = '../plugin'

    def test_message_callback(self, testbot):
        testbot.push_message('test it')
        assert 'Test Result' in testbot.pop_message()
