import os
from distutils.core import setup

# read designative file
def read(f):
    with open(os.path.join(os.path.dirname(__file__), f)) as fd:
        return fd.read()

setup(
    name = 'SOA',
    version = '0.0.1-',
    author = 'wangsong19',
    author_email = '15507484608@163.com',
    description = 'A learning python framework to work with web etc.',
    url = 'https://github.com/wangsong19/soa',
    long_description = read('README.rst'),
    license = 'MIT',
    packages = ['soa', 'soa.web'],
    classifiers = [
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
