#!/usr/bin/env python3
"""
Distutils installation script.

"""

import ast
import os.path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read_version_string(filename):
    """Reads the __version__ string from a python source file.
    """
    path = os.path.join(os.path.dirname(__file__), filename)
    for line in open(path, encoding='utf-8'):
        if line.startswith('__version__'):
            return ast.parse(line).body[0].value.s


def read_readme(filename):
    """Reads a long_description string from a text file.
    """
    path = os.path.join(os.path.dirname(__file__), filename)
    return open(path, encoding='utf-8').read()


setup(
    name='joystickwake',
    version=read_version_string('joystickwake'),
    description="Joystick-aware screen waker",
    long_description=read_readme('README.rst'),
    author='Forest',
    author_email='forestcode@ixio.org',
    url='https://github.com/foresto/joystickwake',
    requires=['pyudev'],
    install_requires=['pyudev'],  # for pip
    scripts=['joystickwake'],
    data_files=[('/etc/xdg/autostart', ['joystickwake.desktop'])],
    platforms=['Linux'],
    license='Expat',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: DFSG approved',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Desktop Environment :: Screen Savers',
        'Topic :: Games/Entertainment',
        'Topic :: System :: Hardware',
        ],
    )
