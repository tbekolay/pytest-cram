#!/usr/bin/env python
import imp
import io
import sys
import os

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import find_packages, setup  # noqa: F811


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

root = os.path.dirname(os.path.realpath(__file__))
version_module = imp.load_source(
    'version', os.path.join(root, 'pytest_cram', 'version.py'))

setup(
    name="pytest-cram",
    version=version_module.version,
    author="Trevor Bekolay",
    author_email="tbekolay@gmail.com",
    packages=find_packages(),
    scripts=[],
    url="https://github.com/tbekolay/pytest-cram",
    license="MIT license",
    description="Run cram tests with pytest.",
    long_description=read('README.rst', 'CHANGES.rst'),
    install_requires=[
        "pytest>=2.8",
        "cram>=0.7",
    ],
    tests_require=[],
    entry_points={
        'pytest11': ['cram = pytest_cram'],
    },
    classifiers=[
        'Framework :: Pytest',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Testing',
    ]
)
