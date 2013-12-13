#!/usr/bin/env python
from setuptools import setup

setup(name='ribbit',
      version='0.1',
      description='ribbit is the perfect collaboration tool for all creators',
      author='giginet',
      author_email='giginet.net@gmail.com',
      url='https://github.com/giginet/ribbit',
      test_suite = "ribbit.runtests.runtests",
      include_paclage_data = True,
      requires=[
        'django (>=1.6.0)',
        'factory_boy (>=2.2.1)'
      ]
)