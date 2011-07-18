Installation instructions
=========================

Install virtualenv
---------------------

projectenv depends on virtualenv, so make sure you have virtualenv installed.

    $ easy_install virtualenv

Download projectenv using git
----------------------------

    $ git clone git@github.com:teaminsight/ProjectEnv.git ~/.projectenv

Edit your shell's configuration file
---------------------------------------

If your shell is Bourne shell compatible (bash, ksh, zsh, etc.), then add the
following lines to your config file:

    export PROJECTENV_HOME=$HOME/.projectenv
    source $PROJECTENV_HOME/bin/projectenv.sh

If your shell is C shell compatible (csh, tcsh, etc.), then add the following
lines to your config file:

    setenv PROJECTENV_HOME $HOME/.projectenv
    alias projectenv 'source $PROJECTENV_HOME/bin/projectenv.csh \!*'

You're done!
---------------

Go have fun creating virtual environments for your project with projectenv. See the
README file for usage instructions.

Updating
-----------

Since projectenv is distributed as a git repository, all you need to do is update
your clone of the projectenv repository.

    $ cd $PROJECTENV_HOME
    $ git pull
