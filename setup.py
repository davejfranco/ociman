from setuptools import setup


setup(
    name = 'ociman',
    description='Commandline tool to interact with oci',
    version = '0.1.0',
    author='Dave Franco',
    author_email='davefranco1987@gmail.com',
    license='MIT',
    packages = ['ociman'],
    entry_points = {
        'console_scripts': [
            'ociman = ociman.__main__:main'
        ]
    })