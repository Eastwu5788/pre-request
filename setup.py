# -*- coding: utf-8 -*-
# (C) Wu Dong, 2018
# All rights reserved
__author__ = 'Wu Dong <wudong@eastwu.cn>'
__time__ = '2018/9/6 11:07'
import os
import sys

from codecs import open

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

packages = ['pre_request']

requires = []

about = {}
with open(os.path.join(here, 'pre_request', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

readme = None

if os.path.exists('README.md'):
    with open('README.md', 'r', 'utf-8') as f:
        readme = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=packages,
    package_data={"": ["LICENSE"], "pre-request": ["*.pem"]},
    package_dir={'pre-request': 'pre-request'},
    include_package_data=True,
    python_requires=">=2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=requires,
    license=about['__license__'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)

