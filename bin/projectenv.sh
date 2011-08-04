#!/bin/sh

__last_exit_status=0

__projectenv__sync() {
    __projectenv__off
    __projectenv__python $*

    if [ $__last_exit_status == 0 ]; then
        __projectenv__on
    fi
}

__projectenv__on() {
    __projectenv__off
    source $PROJECTENV_HOME/environments/$env_name/bin/activate
    source $VIRTUAL_ENV/bin/post_activate.sh
}

__projectenv__off() {
    if [ $VIRTUAL_ENV ]; then
        pre_deactivate=$VIRTUAL_ENV/bin/pre_deactivate.sh
        if [ -e $pre_deactivate ]; then
          source $pre_deactivate
        fi
        deactivate
    fi
}

# Run projectenv.__main__ whether or not a virtualenv is active
__projectenv__python() {
    export _PROJECTENV_OLD_PYTHONPATH=$PYTHONPATH
    export PYTHONPATH=$PROJECTENV_PATH:$PYTHONPATH
    python $PROJECTENV_PATH $*
    __last_exit_status=$?
    export PYTHONPATH=$_PROJECTENV_OLD_PYTHONPATH
    unset _PROJECTENV_OLD_PYTHONPATH
}

projectenv() {
    env_name=`pwd | grep -o -E "[^/]+$"`

    if [ -z $PROJECTENV_PATH ]; then
        export PROJECTENV_PATH=`python -m projectenv.__main__ path`
    fi

    if [[ $1 = 'sync' || $1 = 'on' || $1 = 'off' ]]; then
        # these commands must modify the environment in some way
        "__projectenv__$1" $*
    else
        __projectenv__python $*
    fi
}
