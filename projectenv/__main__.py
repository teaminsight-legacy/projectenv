import os
import sys

from logger import log, error, DEBUG
import commands

COMMANDS = {
    'init': commands.init,
    'sync': commands.sync,
    'path': commands.path
}

def main():
    if DEBUG:
        log('debug', str(True))

    if len(sys.argv) < 2:
        error('usage')
    elif sys.argv[1].lower() in COMMANDS:
        COMMANDS[sys.argv[1].lower()](*sys.argv[2:])
    else:
        error('unknown_command', 'unkown command: %s' % sys.argv[1])

if __name__ == '__main__':
    main()
