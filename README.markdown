projectenv
==========

The easiest way to create virtual environments for your python projects.

Installation
------------

See the [INSTALL](https://github.com/teaminsight/ProjectEnv/blob/master/INSTALL.markdown) file.

Configuring a virtualenv for your project
-----------------------------------------

    cd path/to/your/project
    projectenv init
    vi environment.py # configure to your heart's content
    projectenv sync # This could take a while

At this point, a virtualenv for your project has been created and all of the
packages you specified have been installed. The virtualenv will be active and
ready for you to use.

Activating the virtualenv for a project
---------------------------------------

    cd path/to/your/project
    projectenv on

Deactivating the virtualenv for a project
-----------------------------------------

    projectenv off # works anywhere

The environment.py file
-----------------------

The environment.py file is where you specify the packages you want
installed in your virtualenv as well as the environment variables that
should be present and their values. When you run `projectenv init` an
empty environment.py file is generated for you with two variables
present: the `environment_vars` dict and the `required_libs` list.

Once you have created your environment.py file, you must run `projectenv sync`
to setup the virtualenv for your project. The sync commands
installs all of the python packages listed in required_libs and
generates scripts to setup and restore your shell's environment whenever
you run `projectenv on` or `projectenv off`. Any time you change your
environment.py file, you should run `projectenv sync` to ensure that
your project's virtualenv stays up to date.

### environment_vars

The `environment_vars` dict allows you to specify environment variables
that you want available in your project's virtualenv. projectenv is
careful to save and restore your current shell environment when you run
`projectenv on|off`, so it is safe to specify anything here. Here is a
simple example of an `environment_vars` specification:

```python
environment_vars = {
    'FOO': 'bar'
    'PYTHONPATH': '$HOME/python/my_unreleased_lib'
}
```

Notice that you can even use environment variables from your normal
shell environment in your virtual environment.

### required_libs

The `required_libs` list allows you to specifiy which packages are
installed and in which order they are installed. If a package has
dependencies specified in its `setup.py` file, projectenv will install
those dependencies automatically so you don't need to specify those.
Also, if you have a package you want to install that is not hosted on a
pypi server but is available as a git repository, you can install the
package directly from the git repositiory.

Here is an example `required_libs` specification:

```python
required_libs = [
  'nose',
  'simplejson>=2.1.2,<2.2',
  ('readline', {'install_with': 'easy_install'}),
  ('customlib', {
     'git': 'git://github.com/jbgo/customlib.git',
     'ref': 'experimental'
  })
] + read_requirements()
```

By default, you just need to specify a package name and the latest
version on pypi will be installed. You can also specify specific
versions. projectenv uses pip as the default installer, but you can
specify a custom install command with the `install_with` option.
Installing from a git repo requires the `git` option specifying the
absolute URL of the repo. You can also specify a particular branch, tag,
or commit with the `ref` option. Also, if you have a `requirements.txt`
file for your project, you can include those automatically by calling
the `read_requirements()` function.

### Predefined values

The following variables are available for you to use in your
`environment.py` file:

VIRTUAL_ENV - The path to your project's virtual environment.

PROJECTENV_HOME - ~/.projectenv

SITE_PACKAGES - The path to your project's virtual site-packages
directory.

### Helper functions

The following helper functions are available for you to use in your
`environment.py` file.

**read_requirements(path='requirements.txt')** - Returns an array of
requirements from your project's requirements.txt file.

**install_src_dir(*rel_path)** - Appends path components to the source
directory for packages installed from a git repository and returns the
absolute path. For example, `install_src_dir('customlib', 'VERSION')`
returns `/home/you/.projectenv/src/customlib/VERSION`.

**site_packages_dir(*rel_path)** - Appends path components to the
site-packages directory for your virtualenv. For example,
`site_packages_dir('some-package.egg', 'configure.py')` returns
`/home/you/.projectenv/your-project/lib/python2.6/site-packages/some-package.egg/configure.py'`.

Installing packages from alternate python servers
-------------------------------------------------

If you have packages hosted on a local or internal pypi server, and you
have configured your `~/.pypirc` file to include those servers, projectenv
will automatically detect those servers and install packages from them.
For example, if you had the following `~/.pypirc` file, projectenv will
attempt to install packages from pypi.internal.com:6789:

```
[distutils]
index-servers =
    pypi
    internal

[internal]
repository:http://pypi.internal.com:6789
```
