import os
from logger import log, error, DEBUG
from cmdrunner import add_checkpoint, run, cd, cp, rm, mkdir
from package_manager import install_libs
from scriptgen import ScriptGenerator
import spec_helpers

start_dir = os.getcwd()
home_dir = os.getenv('PROJECTENV_HOME')
env_name = os.path.basename(os.getcwd())
env_path = os.path.join(home_dir, 'environments', env_name)
spec_path = './environment.py'
env_prefix = '_PROJECTENV_'

def revert_init():
    rm('./environment.py')

def init():
    cp(os.path.join(home_dir, 'specs', 'default.py'), spec_path)
    add_checkpoint(revert_init)
    # TODO: ensure env_name is unique
    run('virtualenv', '--no-site-packages', env_path)

def sync():
    spec = get_spec()
    if 'required_libs' in spec:
        install_libs(spec['required_libs'])
        # TODO: generate_requirements_txt(spec['required_libs'])

    log('-')
    generate_post_activate_script(spec)

    log('-')
    generate_pre_deactivate_script(spec)

##
# helper methods for the main commands
##

def get_spec():
    spec_globals = {
        'VIRTUAL_ENV': env_path,
        'PROJECTENV_HOME': home_dir,
        'SITE_PACKAGES': 'lib/python2.6/site-packages',
        'read_requirements': spec_helpers.read_requirements,
        'install_src_dir': spec_helpers.install_src_dir,
        'site_packages_dir': spec_helpers.site_packages_dir
    }
    spec = {}

    execfile(spec_path, spec_globals, spec)
    return spec

def generate_post_activate_script(spec):
    env = freeze_env(get_env_for(spec))
    script = ScriptGenerator(env)
    script.write(os.path.join(env_path, 'bin', 'post_activate'))

def generate_pre_deactivate_script(spec):
    env = unfreeze_env(freeze_env(get_env_for(spec)))
    script = ScriptGenerator(env)
    script.write(os.path.join(env_path, 'bin', 'pre_deactivate'))

def get_env_for(spec):
    env = spec.get('environment_vars') or {}
    if not 'PYTHONPATH' in env:
        env['PYTHONPATH'] = None
    return env

def freeze_env(env):
    """
    Prefix any environment variables we could potentially overwrite with
    '_PROJECTENV_' so we can restore the original environment on deactivation.

    """
    frozen = {}
    for k, v in env.iteritems():
        if os.getenv(k):
            frozen[env_prefix + k] = '$' + k
        frozen[k] = v
    return frozen

def unfreeze_env(frozen_env):
    """
    Basically the inverse of freeze_env, but will set values to None if they
    can safely be unset.

    """
    unfrozen = {}
    for k, v in frozen_env.iteritems():
        if k.startswith(env_prefix):
            unfrozen[k.replace(env_prefix, '')] = '$' + k # restore to original
            unfrozen[k] = None # unset prefix version
        elif (env_prefix + k) not in frozen_env:
            unfrozen[k] = None # safe to unset
    return unfrozen
