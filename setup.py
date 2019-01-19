import re
from setuptools import setup, find_packages

# Load version from module (without loading the whole module)
with open('src/bext/__init__.py', 'r') as fo:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fo.read(), re.MULTILINE).group(1)

# Read in the README.md for the long description.
with open('README.md') as fo:
    long_description = fo.read()

setup(
    name='Bext',
    version=version,
    url='https://github.com/asweigart/bext',
    author='Al Sweigart',
    author_email='al@inventwithpython.com',
    description=('''A cross-platform Python 2/3 module for colorful, boring, text-based terminal programs.'''),
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    test_suite='tests',
    install_requires=['colorama==0.4.1'],
    keywords='',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
