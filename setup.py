# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from frules import __version__ as version
import os

def strip_comments(l):
    return l.split('#', 1)[0].strip()

def reqs(*f):
    return list(filter(None, [strip_comments(l) for l in open(
        os.path.join(os.getcwd(), *f)).readlines()]))

install_requires = reqs('requirements.txt')

setup(
    name='frules',
    version=version,
    description='simple functional fuzzy rules implementation',
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
    ],
    # Make setuptools include all data files under version control,
    # svn and CVS by default
    include_package_data=True,
    zip_safe=False,
    # Tells setuptools to download setuptools_hg before running setup.py so
    # it can find the data files under Hg version control.
    setup_requires=['setuptools_hg'],
    install_requires=install_requires,
)