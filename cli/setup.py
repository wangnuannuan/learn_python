import os

from setuptools import setup, find_packages

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), 'r') as f:
        return f.read()

def read_requirements():
    req_lines = read('requirements.txt').splitlines()
    return [req for req in req_lines if len(req) > 0 and not req.startswith("#")]

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
            "embarc=embarc_tools.main:main",
        ]
    },
    install_requires = read_requirements(),
    include_package_data = True,
)
