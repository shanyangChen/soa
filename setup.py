
from disutils.core import setup

setup(
    name = 'SOA',
    verison = '0.0.1',
    python_require = '>=3.6',
    author = 'wangsong',
    author_email = '15507484608@163.com',
    description = 'A learning python framework to work with web etc.'
    long_description = read('README.md'),
    license = 'MIT License',
    packages = ['soa'],
    platform = 'any',
    classifiers = [
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
