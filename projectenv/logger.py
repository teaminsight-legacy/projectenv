import sys

DEBUG = False

ERRORS = {
    'usage': (1, 'projectenv <command> [...]'),
    'unknown_command': (2, 'unkown command'),
    'missing_env_name': (3, 'missing environment name')
}

def log(prompt='info', message=''):
    if not prompt:
        print message
    elif prompt == '-':
        print '\n' + '-' * 50
    else:
        print '[projectenv: %s] %s' % (prompt, message)

def error(error_key, message=None, fatal=True):
    err = ERRORS[error_key]
    log('ERROR', message or err[1])
    sys.exit(err[0])
