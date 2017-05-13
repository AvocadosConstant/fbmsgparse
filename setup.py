from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fbmsgparse',

    version='1.0',

    description='A simple python package to clean, organize, preprocess, and make sense of your entire Facebook message history.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/AvocadosConstant/fb-messages-parser',

    # Author details
    author='Tim Hung',
    author_email='thung1@binghamton.edu',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='facebook messages parsing preprocessing',

    packages=find_packages(),

    install_requires=['bs4'],
)
