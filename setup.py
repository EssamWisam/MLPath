# pylint: skip-file
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

def read_requirements():
    """Read requirements from requirements.txt."""
    with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
        requirements = f.read().splitlines()
    return requirements


# This call to setup() does all the work
setup(
    name="mlpath",
    version="1.0.32",
    description="A lightweight api for machine and deep learning experiment logging in the form of a python library. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mlpath.readthedocs.io/",
    author="Essam W., Abdullah A.",
    author_email="essamwisam@outlook.com",
    license="GPLv3",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["mlpath", "mlpath.mlquest", "mlpath.mldir_cli"],
    include_package_data=True,
    package_data={'mldir':['*.zip', '*.png', '*pdf', '*jpeg','*ipynb', '*html', '*css', '*pkl', '*js']},
    install_requires=['varname', 'click', 'flask'],
    entry_points='''
    [console_scripts]
    mldir=mlpath.mldir_cli.cli:main
    mlweb=mlpath.mldir_cli.cli:web
    '''
)

# Steps to upload to PyPI
# 0 - Increment the version number in setup.py
# 1 - Remove the dist folder
# 2- python3 setup.py sdist bdist_wheel  
# 3 - twine upload dist/*