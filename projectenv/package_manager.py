import sys
import os
import re
import pkg_resources
from ConfigParser import ConfigParser
from urlparse import urljoin

from logger import log, error, DEBUG
from cmdrunner import add_checkpoint, run, cd, cp, rm, mkdir

def install_libs(required_libs):
    for lib_spec in required_libs:
        if isinstance(lib_spec, str):
            install_lib(lib_spec)
        else:
            install_lib(lib_spec[0], lib_spec[1])

def install_lib(lib_name, options={}):
    if already_installed(lib_name, options):
        log('-')
        log('install',
            "'%s' and all dependencies are already installed" % lib_name)
    else:
        log('-')
        log('installing', lib_name)
        if 'install_with' in options:
            custom_install(lib_name, options)
        else:
            pip_install(lib_name, options)
        post_install(lib_name, options)
        log('installation complete')

def already_installed(lib_spec, options, working_set=None):
    """
    returns True if a package matching the given requirement is already
    installed and all the dependencies are already installed. If
    options['path'] is present, already_installed() returns False. This allows
    local copies of a library to shadow installed versions while they are being
    developed.

    """
    if 'path' in options:
        return False

    if not working_set:
        working_set=pkg_resources.WorkingSet(sys.path)

    try:
        working_set.require(lib_spec)
    except pkg_resources.ResolutionError:
        return False
    else:
        return True

def pip_install(lib_name, options):
    virtual_env = os.getenv('VIRTUAL_ENV')
    requirement = pip_requirement(lib_name, options)
    req_file = os.path.join(virtual_env, 'install-requirements.txt')
    write_requirement(requirement, req_file)
    extra_repos = ['--extra-index-url=' + repo_url
                   for repo_url in extra_pypi_index_servers()]
    run('pip', 'install', '-E', virtual_env, '-r', req_file,
        *extra_repos)

def extra_pypi_index_servers(pypirc_path=None):
    config = ConfigParser()
    if not pypirc_path:
        pypirc_path = os.path.join(os.getenv('HOME', ''), '.pypirc')
    config.read(pypirc_path)
    return [urljoin(config.get(section, 'repository'), 'simple')
            for section in config.sections()
            if 'repository' in dict(config.items(section))]

def custom_install(lib_name, options):
    install_cmd = options['install_with']
    run(install_cmd, lib_name)

def post_install(lib_name, options):
    if 'post_install' in options:
        # TODO: some working directory magic
        for cmd in options['post_install']:
            run(*cmd)

def pip_requirement(lib_name, options):
    if 'path' in options:
        lib_name = lib_name_without_version(lib_name)
        req = '-e %s' % options['path']
    elif 'git' in options:
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
