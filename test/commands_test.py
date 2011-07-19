import unittest
import os
import shutil
from copy import copy

from test import run_commands, reset_run_commands

from projectenv import commands

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


class PathCommandTestCase(unittest.TestCase):

    def test_path(self):
        self.assertEqual(commands.path(), os.path.abspath('./projectenv'))


class InitCommandTestCase(unittest.TestCase):

    project_dir = os.path.join(os.getcwd(), 'test', 'project_test_virtual_env')
    project_env_home = os.path.join(os.getcwd(), 'test')
    env_file = 'environment.py'
    test_env = os.path.join(os.getcwd(), 'test', 'environments',
            'project_test_virtual_env')

    def setUp(self):
        os.environ['PROJECTENV_HOME'] = self.project_env_home
        os.environ['VIRTUAL_ENV'] = self.test_env
        reset_run_commands()
        os.makedirs(self.project_dir)
        os.chdir(self.project_dir)

    def tearDown(self):
        if os.path.exists(self.project_dir):
            shutil.rmtree(self.project_dir)
        if os.path.exists(self.test_env):
            shutil.rmtree(self.test_env)
        os.chdir(os.path.join(self.project_env_home, '..'))

    def touch(self, path):
        f = open(path, 'w')
        f.close()

    def test_init(self):
        """should create an environment.py file and new virtualenv"""
        commands.init()
        self.assertEqual(run_commands(), [
            'cp %s ./%s' % (os.path.join(self.project_env_home,
                'specs', 'default.py'), self.env_file),
            'virtualenv --no-site-packages %s' % self.test_env
        ])

    def test_spec_exists(self):
        """should not create a new environment file"""
        f = open(os.path.join(self.project_dir, self.env_file), 'w')
        f.close()

        commands.init()
        self.assertEqual(run_commands(), [
            'virtualenv --no-site-packages %s' % self.test_env
        ])

    def test_virtualenv_exists(self):
        """should not create a new virtualenv or environment file"""
        f = open(os.path.join(self.project_dir, self.env_file), 'w')
        f.close()
        os.makedirs(self.test_env)

        commands.init()
        self.assertEqual(run_commands(), [])
