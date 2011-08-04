import unittest
import os
import sys

from projectenv import spec_helpers

class SpecHelpersTestCase(unittest.TestCase):

    test_env = os.path.join(os.getcwd(), 'test', 'projectenv_test_virtual_env')

    def setUp(self):
        os.environ['VIRTUAL_ENV'] = self.test_env

    def test_read_requirements(self):
        """
        should return a list of requirements from the requirements.txt file

        """
        requirements = ['foo', 'bar>=0.1.2', 'biz>=0.2.3,<0.3.0', 'baz==1.0.1']
        with open('requirements.txt', 'w') as f:
            f.write('\n'.join(requirements) + '\n')
        self.assertEqual(spec_helpers.read_requirements(), requirements)
        os.remove('requirements.txt')

    def test_read_missing_requirements(self):
        """should return an emtpy list when requirements.txt is missing"""
        self.assertEqual(spec_helpers.read_requirements(), [])

    def test_install_src_dir(self):
        """
        should return the path where a pip install checks out its git repos

        """
        self.assertEqual(spec_helpers.install_src_dir(),
                os.path.join(self.test_env, 'src'))

    def test_install_src_dir_with_path_components(self):
        """
        should return the path where a pip install checks out its git repos
        joined with any relative path components

        """
        a = 'foo/bar'
        b = 'biz/baz'
        self.assertEqual(spec_helpers.install_src_dir(a, b),
                os.path.join(self.test_env, 'src', a, b))

    def test_site_packages_dir(self):
        """
        should return the site packages path for the active virtual environment

        """
        self.assertEqual(spec_helpers.site_packages_dir(), os.path.join(
            self.test_env, 'lib/python%s/site-packages' % sys.version[:3]))

    def test_site_packages_dir_with_path_components(self):
        """
        should return the site packages path for the active virtual environment
        joined with any relative path components

        """
        a = 'foo/bar'
        b = 'biz/baz'
        self.assertEqual(spec_helpers.site_packages_dir(a, b), os.path.join(
            self.test_env, 'lib/python%s/site-packages' % sys.version[:3],
            a, b))

