import os
import re

from logger import log, error, DEBUG
from cmdrunner import add_checkpoint, run, cd, cp, rm, mkdir

def install_libs(required_libs):
    for lib_spec in required_libs:
        if isinstance(lib_spec, str):
            install_lib(lib_spec)
        else:
            install_lib(lib_spec[0], lib_spec[1])

def install_lib(lib_name, options={}):
    log('-')
    log('installing', lib_name)
    if 'install_with' in options:
        custom_install(lib_name, options)
    else:
        pip_install(lib_name, options)
    post_install(lib_name, options)
    log('installation complete')

def pip_install(lib_name, options):
    virtual_env = os.getenv('VIRTUAL_ENV')
    requirement = pip_requirement(lib_name, options)
    req_file = os.path.join(virtual_env, 'install-requirements.txt')
    write_requirement(requirement, req_file)
    run('pip', 'install', '-r', req_file)

def custom_install(lib_name, options):
    install_cmd = options['install_with']
    run(install_cmd, lib_name)

def post_install(lib_name, options):
    if 'post_install' in options:
        # TODO: some working directory magic
        for cmd in options['post_install']:
            run(*cmd)

def pip_requirement(lib_name, options):
    if 'git' in options:
        lib_name = lib_name_without_version(lib_name)
        ref = ('@' + options['ref']) if 'ref' in options else ''
        req = '-e git+%s%s#egg=%s' % (options['git'], ref, lib_name)
    else:
        req = lib_name
    return req

def lib_name_without_version(lib_name):
    return re.split(r'(<|>|=|,)', lib_name)[0]

def write_requirement(requirement, path):
    f = open(path, 'w')
    try:
        f.write(requirement)
    finally:
        f.close()
