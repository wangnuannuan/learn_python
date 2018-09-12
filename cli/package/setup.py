import os

from setuptools import setup, find_packages

setup(
    name='embarc_cli',
    version='0.0.1',
    description='',
    author='',
    author_email='',
    keywords="",
    url="",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            "embarc_tools=tools.main:main",
            "embarc=tools.main:main",
        ]
    },
    include_package_data = True,
)