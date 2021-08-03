import sys
import os
from setuptools import setup, find_packages


with open(os.getcwd() + '\\requirements.txt') as file:
    requires = file.readlines()

if sys.version_info.minor < 7:
    requires.append('dataclasses')

with open(os.getcwd() + '\\README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='lc3asm',
    version='0.0.1',
    author='d0rj',
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    url='https://github.com/d0rj/LC3_asm',
    project_urls={
        'Bug Tracker': 'https://github.com/d0rj/LC3_asm/issues',
    },
    description='Assembler for LC3 machine',
    long_description=long_description,
    long_description_content_type='text/markdown',

    packages=find_packages(),
    install_requires=requires,
    package_data={
        'grammar': ['grammar/lc3_assembly.lark'],
        'requirements': ['requirements.txt']
    },
)
