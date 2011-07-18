import os
os.environ['PROJECTENV_HOME'] = os.path.join(os.getcwd(), '..')

# We don't actually want to run any of these commands in our unit tests because
# they just won't work and it could have unintended side effects like files and
# directories being created, deleted, and modified.
import cmdrunner

_run_commands = []

def _run(*args, **kwargs):
    _run_commands.append(' '.join(args))

def _cp(source, dest):
    _run_commands.append('cp %s %s' % (source, dest))

cmdrunner.run = _run
cmdrunner.cp = _cp

def run_commands():
    """
    returns a list of all the commands the cmdrunner has run since the last
    time it was reset

    """
    return _run_commands

def reset_run_commands():
    """
    reset the list of commands run by the cmdrunner

    """
    global _run_commands
    _run_commands = []
