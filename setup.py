import sys
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = 'ociman',
    description='Commandline tool to automate oci ops',
    version = '0.1.0',
    author='Dave Franco',
    author_email='davefranco1987@gmail.com',
    license='Apache License 2.0',
    packages = ['ociman'],
    install_requires =required,
    entry_points = {
        'console_scripts': [
            'ociman = ociman.__main__:main'
        ]
    })