import unittest
import os
import shutil
import pkg_resources

from nose.plugins.skip import SkipTest
from test import run_commands, reset_run_commands

from projectenv.spec_helpers import read_requirements as reqlist
from projectenv import package_manager

class PackageManagerTestCase(unittest.TestCase):

    test_env = os.path.join(os.getcwd(), 'test', 'projectenv_test_virtual_env')
    req_path = os.path.join(test_env, 'install-requirements.txt')

    def setUp(self):
        self.old_home = os.getenv('HOME')
        os.environ['HOME'] = os.path.abspath('.')
        reset_run_commands()
        os.environ['VIRTUAL_ENV'] = self.test_env
        os.mkdir(os.getenv('VIRTUAL_ENV'))

    def tearDown(self):
        os.environ['HOME'] = self.old_home
        shutil.rmtree(os.getenv('VIRTUAL_ENV'))

    def test_string_req(self):
        package_manager.install_lib('foo')
        self.assertTrue(os.path.exists(self.req_path))
        self.assertEqual(reqlist(self.req_path), ['foo'])
        self.assertEqual(run_commands(), ['pip install -E %s -r %s' % (
            self.test_env, self.req_path)])

    def test_string_req_with_version(self):
        package_manager.install_lib('foo==1.2.3')
        self.assertTrue(os.path.exists(self.req_path))
        self.assertEqual(reqlist(self.req_path), ['foo==1.2.3'])
        self.assertEqual(run_commands(), ['pip install -E %s -r %s' % (
            self.test_env, self.req_path)])


    def test_git_req(self):
        cwd = os.getcwd()
        os.makedirs(os.path.join(self.test_env, 'src', 'foo'))
        package_manager.install_lib('foo', {'git': 'ssh://test.repo/foo'})
        self.assertTrue(os.path.exists(self.req_path))
        self.assertEqual(reqlist(self.req_path), [
            '-e git+ssh://test.repo/foo#egg=foo'
        ])
        self.assertEqual(run_commands(), ['pip install -E %s -r %s' % (
            self.test_env, self.req_path)])
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
        self.assertEqual(run_commands(), ['pip install -E %s -r %s' % (
            self.test_env, self.req_path)])
        self.assertEqual(os.getcwd(), cwd) # ensure we're back where we started

    def test_path_req(self):
        cwd = os.getcwd()
        lib_path = os.path.join(self.test_env, 'foo', 'bar')
        os.makedirs(lib_path)
        package_manager.install_lib('bar', {'path': lib_path})
        self.assertTrue(os.path.exists(self.req_path))
        self.assertEqual(reqlist(self.req_path), [
            '-e %s' % lib_path
        ])
        self.assertEqual(run_commands(), ['pip install -E %s -r %s' % (
            self.test_env, self.req_path)])

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
            'pip install -E %s -r %s' % (self.test_env, self.req_path),
            'cp foo bar'
        ])

class AlreadyInstalledTestCase(unittest.TestCase):

    def setUp(self):
        reset_run_commands()
        ws = pkg_resources.WorkingSet([])
        dist = pkg_resources.Distribution.from_filename('.')
        ws.add(dist)
        self.working_set = ws

    def test_package_not_installed(self):
        self.assertEqual(False, package_manager.already_installed('foo', {},
                    self.working_set))

    def test_package_installed(self):
        self.assertTrue(package_manager.already_installed('projectenv', {},
            self.working_set))

    def test_local_packages(self):
        self.assertTrue(package_manager.already_installed('projectenv', {}))

    def test_bad_requirement(self):
        self.assertRaises(ValueError, package_manager.already_installed,
                'foo/bar', {}, self.working_set)

    def test_skip_install(self):
        package_manager.install_lib('projectenv', {})
        self.assertEqual(run_commands(), [])

    def test_local_installed(self):
        self.assertEqual(package_manager.already_installed('projectenv',
                {'path': 'foo'}, self.working_set), False)


class PypircTestCase(unittest.TestCase):

    test_env = os.path.join(os.getcwd(), 'test', 'projectenv_test_virtual_env')
    req_path = os.path.join(test_env, 'install-requirements.txt')

    def setUp(self):
        reset_run_commands()
        self.old_home = os.getenv('HOME')
        os.environ['HOME'] = os.path.abspath('test/fixtures')
        os.environ['VIRTUAL_ENV'] = self.test_env
        os.mkdir(os.getenv('VIRTUAL_ENV'))

    def tearDown(self):
        os.environ['HOME'] = self.old_home
        shutil.rmtree(os.getenv('VIRTUAL_ENV'))

    def test_missing_pypirc(self):
        """should return an empty list if .pypirc is missing"""
        self.assertEqual(
                package_manager.extra_pypi_index_servers('does not exist'),
                [])


    def test_no_extra_pypi_servers(self):
        """
        should return empty list when no additional pypi servers are
        specified in .pypirc

        """
        pypirc = 'test/fixtures/pypirc-default.txt'
        self.assertEqual(package_manager.extra_pypi_index_servers(pypirc), [])

    def test_extra_pypi_servers(self):
        """
        should return a list of URLs for any additional python servers
        specified in .pypirc

        """
        pypirc = 'test/fixtures/pypirc-extra.txt'
        self.assertEqual(package_manager.extra_pypi_index_servers(pypirc), [
            'http://localhost:8000/simple',
            'http://pypi.internal.com/simple'
        ])

    def test_extra_pypi_servers_with_no_arg(self):
        """should use $HOME/.pypirc when no arg is given"""
        self.assertEqual(package_manager.extra_pypi_index_servers(), [
            'http://localhost:8000/simple',
            'http://pypi.internal.com/simple'
        ])

    def test_pip_install_with_extra_pypi_servers(self):
        """
        should include --extra-index-url options when additional pypi servers
        are specified in .pypirc

        """
        package_manager.install_lib('foo')
        self.assertEqual(run_commands(), [
            'pip install -E %s -r %s --extra-index-url=%s --extra-index-url=%s' % (
                self.test_env,
                self.req_path,
                'http://localhost:8000/simple',
                'http://pypi.internal.com/simple'
            )
        ])
