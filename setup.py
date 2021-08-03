import sys
from setuptools import setup, find_packages


with open('./requirements.txt') as file:
    requires = file.readlines()

if sys.version_info.minor < 7:
    requires.append('dataclasses')

setup(
    name="lc3_asm",
    packages=find_packages(),
    install_requires=requires
)
