"""
Methods you can use in your environment.py file

You do not need to require these, they will already be available.
"""
import os
import sys

def read_requirements(path='requirements.txt'):
    """returns a list of entries in the requirements.txt file"""
    f = open(path)
    reqs = []
    try:
        for line in f:
            if line.strip():
                reqs.append(line.strip())
    finally:
        f.close()
    return reqs

def install_src_dir(*rel_path):
    """
    returns the the source path for repos checked out by a pip install joined
    with any relative path components

    """
    return os.path.join(os.getenv('VIRTUAL_ENV'), 'src', *rel_path)

def site_packages_dir(*rel_path):
    """
    returns the the active virtualenv's site packages path joined with any
    relative path components

    """
    return os.path.join(os.getenv('VIRTUAL_ENV'), 'lib',
            'python%s' % sys.version[:3], 'site-packages', *rel_path)
