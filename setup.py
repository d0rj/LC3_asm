from setuptools import setup, find_packages


with open('./requirements.txt') as file:
    requires = file.readlines()

setup(
    name="lc3_asm",
    packages=find_packages(),
    install_requires=requires
)
