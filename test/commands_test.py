import unittest
import os
from copy import copy

import commands

class CommandsTestCase(unittest.TestCase):

    def setUp(self):
        self._original_environ = copy(os.environ)

    def tearDown(self):
        os.environ = self._original_environ

    def test_get_env_for_without_pythonpath(self):
        """should set PYTHONPATH to nothing if it is not specified"""
        spec = {'environment_vars': {'FOO': 'bar'}}
        self.assertEqual(commands.get_env_for(spec), {
            'FOO': 'bar',
            'PYTHONPATH': None
        })

    def test_get_env_for_with_pythonpath(self):
        """should leave PYTHONPATH alone if it is specified"""
        spec = {'environment_vars': {'FOO': 'bar', 'PYTHONPATH': 'foo'}}
        self.assertEqual(commands.get_env_for(spec), spec['environment_vars'])

    def test_freeze_env(self):
        """should save original environment variables before activation"""
        os.environ = {'foo': 'bar', 'biz': 'baz'}
        env = {'foo': 'boo', 'bing': 'bang'}
        result = commands.freeze_env(env)
        self.assertEqual(result, {'_PROJECTENV_foo': '$foo', 'foo': 'boo',
            'bing': 'bang'})

    def test_unfreeze_env(self):
        """
        should unfreeze the environment so it will appear unmodified after
        virtualenv is deactivated

        """
        frozen = {'_PROJECTENV_foo': '$foo', 'foo': 'boo', 'bing': 'bang'}
        result = commands.unfreeze_env(frozen)
        self.assertEqual(result, {'foo': '$_PROJECTENV_foo', 'bing': None,
            '_PROJECTENV_foo': None})
