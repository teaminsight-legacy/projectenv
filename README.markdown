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

Once you have created your environment.py file, you must run `projectenv
sync` to setup the virtualenv for your project. The sync commands
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
    'PYTHONPATH': '/Users/jbgo/projects/python/my_unreleased_lib'
}
```

### required_libs

TODO - order, versions, options(git, ref, post_install)

### predefined values

**VIRTUAL_ENV** - TODO
**PROJECTENV_HOME** - TODO
**SITE_PACKAGES** - TODO

### helper functions

**read_requirements(path='requirements.txt')** - TODO

**install_src_dir(*rel_path)** - TODO

**site_packages_dir(*rel_path) - TODO
