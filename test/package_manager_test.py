import unittest
import os
import shutil

from test import run_commands, reset_run_commands

from projectenv.spec_helpers import read_requirements as reqlist
from projectenv import package_manager

class PackageManagerTestCase(unittest.TestCase):

    test_env = os.path.join(os.getcwd(), 'test', 'projectenv_test_virtual_env')
    req_path = os.path.join(test_env, 'install-requirements.txt')

    def setUp(self):
        reset_run_commands()
        os.environ['VIRTUAL_ENV'] = self.test_env
        os.mkdir(os.getenv('VIRTUAL_ENV'))

    def tearDown(self):
        shutil.rmtree(os.getenv('VIRTUAL_ENV'))

    def test_string_req(self):
        package_manager.install_lib('foo')
        self.assertTrue(os.path.exists(self.req_path))
        self.assertEqual(reqlist(self.req_path), ['foo'])
        self.assertEqual(run_commands(), ['pip install -r %s' % self.req_path])

    def test_string_req_with_version(self):
        package_manager.install_lib('foo==1.2.3')
        self.assertTrue(os.path.exists(self.req_path))
        self.assertEqual(reqlist(self.req_path), ['foo==1.2.3'])
        self.assertEqual(run_commands(), ['pip install -r %s' % self.req_path])


    def test_git_req(self):
        cwd = os.getcwd()
        os.makedirs(os.path.join(self.test_env, 'src', 'foo'))
        package_manager.install_lib('foo', {'git': 'ssh://test.repo/foo'})
        self.assertTrue(os.path.exists(self.req_path))
        self.assertEqual(reqlist(self.req_path), [
            '-e git+ssh://test.repo/foo#egg=foo'
        ])
        self.assertEqual(run_commands(), ['pip install -r %s' % self.req_path])
        self.assertEqual(os.getcwd(), cwd) # ensure we're back where we started

    def test_git_req_with_ref(self):
        cwd = os.getcwd()
        os.makedirs(os.path.join(self.test_env, 'src', 'foo'))
        package_manager.install_lib('foo>=0.1.0,<0.2.0', {
            'git': 'ssh://test.repo/foo',
            'ref': 'v0.1.4'
        })
        self.assertTrue(os.path.exists(self.req_path))
        self.assertEqual(reqlist(self.req_path), [
            '-e git+ssh://test.repo/foo@v0.1.4#egg=foo'
        ])
        self.assertEqual(run_commands(), ['pip install -r %s' % self.req_path])
        self.assertEqual(os.getcwd(), cwd) # ensure we're back where we started

    def test_custom_req(self):
        package_manager.install_lib('foo', {
            'install_with': 'easy_install'
        })
        self.assertEqual(run_commands(), ['easy_install foo'])

    def test_post_install(self):
        package_manager.install_lib('foo', {
            'post_install': [['cp', 'foo', 'bar']]
        })
        self.assertTrue(os.path.exists(self.req_path))
        self.assertEqual(reqlist(self.req_path), ['foo'])
        self.assertEqual(run_commands(), [
            'pip install -r %s' % self.req_path,
            'cp foo bar'
        ])
