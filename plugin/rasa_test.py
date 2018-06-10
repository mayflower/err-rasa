
import os
import unittest
from plugin.rasa import Rasa
from errbot.backends.test import testbot
from errbot.plugin_manager import PluginManager

class TestRasa(object):
    extra_plugin_dir = '../plugin'

    def test_message_callback(self, testbot):
        testbot.push_message('test it')
        assert 'Test Result' in testbot.pop_message()
