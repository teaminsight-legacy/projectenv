import os
os.environ['PROJECTENV_HOME'] = os.path.join(os.getcwd(), '..')

# We don't actually want to run any of these commands in our unit tests because
# they just won't work and it could have unintended side effects like files and
# directories being created, deleted, and modified.
import cmdrunner
_run_commands = []
def _run(*args, **kwargs):
    print 'args: %s' % str(args)
    _run_commands.append(' '.join(args))
cmdrunner.run = _run

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
