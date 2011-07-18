import os
import subprocess
import shutil
from logger import log, error, DEBUG

rolling_back = False
rollback_stack = []

def run(*command, **kwargs):
    """run a command, print it, and rollback if it fails"""
    log('command', ' '.join(command))

    if DEBUG:
        exit_status = 0
    else:
        exit_status = subprocess.call(command, **kwargs)

    if exit_status != 0:
        log('ERROR', 'last command failed with status %d' % exit_status)
        if not rolling_back: # Don't rollback failed rollbacks
            rollback()
        raise RuntimeError("Command failed, rollback complete")
    return exit_status

def add_checkpoint(rollback_function):
    """push a rollback function onto the stack to undo things if something goes
    wrong"""
    rollback_stack.append(rollback_function)

def rollback():
    log('rolling back')
    rolling_back = True
    while len(rollback_stack) > 0:
        func = rollback_stack.pop()
        func()

##
# wrappers for commands also implemented by the python standard library
##

def cd(path):
    if not DEBUG:
        os.chdir(path)
    log('working dir', path)

def cp(source, dest):
    if not DEBUG:
        shutil.copyfile(source, dest)
    log('copied', "'%s' => '%s'" % (source, dest))

def rm(path):
    if not DEBUG:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)
    log('deleted', path)

def mkdir(path):
    if not DEBUG and not os.path.exists(path):
        os.makedirs(path)
    log('created dir', path)
