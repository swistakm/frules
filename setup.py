# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

from frules import __version__ as version


def read_md(path):
    with open(path, 'r') as f:
        return f.read()


INSTALL_REQUIRES = []
TEST_REQUIRES = ['py.test']
README = os.path.join(os.path.dirname(__file__), 'README.md')

setup(
    name='frules',
    version=version,
    description='simple functional fuzzy rules implementation',
    long_description=read_md(README),
    long_description_content_type="text/markdown",
    author='Michał Jaworski',
    author_email='swistakm@gmail.com',
    url='https://github.com/swistakm/frules',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    # Make setuptools include all data files under version control,
    # svn and CVS by default
    include_package_data=True,
    zip_safe=False,
    setup_requires=['setuptools_git'],
    install_requires=INSTALL_REQUIRES,
    tests_require=TEST_REQUIRES,
)
