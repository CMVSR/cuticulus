# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='cuticle_analysis',
    version='0.0.1',
    description='Project for analyzing ant head images.',
    long_description=readme,
    author='Noah Gardner',
    author_email='ngardn10@students.kennesaw.edu',
    url='https://github.com/ngngardner/cuticle_analysis',
    license=license,
    packages=[
        "cuticle_analysis",
        "cuticle_analysis/assets",
        "cuticle_analysis/antweb",
        "cuticle_analysis/core",
        "cuticle_analysis/datasets",
        "cuticle_analysis/models"
    ],
    entry_points='''
        [console_scripts]
        cuticle_analysis=cuticle_analysis:main
    '''
)
