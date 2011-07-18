#!/bin/sh

__projectenv__sync() {
    source $PROJECTENV_HOME/environments/$env_name/bin/activate
    python $PROJECTENV_HOME/bin/projectenv.py $*
    if [ $? ]; then
        deactivate
        __projectenv__on
    else
        deactivate
    fi
}

__projectenv__on() {
    if [ $VIRTUAL_ENV ]; then
        __projectenv__off
    fi
    source $PROJECTENV_HOME/environments/$env_name/bin/activate
    source $VIRTUAL_ENV/bin/post_activate.sh
}

__projectenv__off() {
    if [ $VIRTUAL_ENV ]; then
        source $VIRTUAL_ENV/bin/pre_deactivate.sh
        deactivate
    fi
}

projectenv() {
    env_name=`pwd | grep -o -E "[^/]+$"`

    if [[ $1 = 'sync' || $1 = 'on' || $1 = 'off' ]]; then
        # these commands must modify the environment in some way
        "__projectenv__$1" $*
    else
        python $PROJECTENV_HOME/bin/projectenv.py $*
    fi
}
