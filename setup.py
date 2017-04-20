import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
      name='recsys_data_pipeline',
      version='1.0',
      install_requires=[],
      packages=find_packages(),
    )