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
