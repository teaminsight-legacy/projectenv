from setuptools import setup
import os
from glob import glob

def files_to_distribute():
    base_dir = os.path.expanduser('~/.projectenv')
    return [
        (base_dir, ['README.markdown', 'INSTALL.markdown']),
        (os.path.join(base_dir, 'bin'), glob('bin/*')),
        (os.path.join(base_dir, 'specs'), glob('specs/*'))
    ]

setup(name='projectenv',
      version='0.0.4',
      description='The easiest way to create virtual environments for your python projects',
      author='Jordan Bach',
      author_email='jordanbach@gmail.com',
      url='https://github.com/teaminsight/projectenv',
      packages=['projectenv'],
      data_files = files_to_distribute()
)
