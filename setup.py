#!/usr/bin/env python
from setuptools import setup

setup(name='ribbit',
      version='0.1',
      description='ribbit is the perfect collaboration tool for all creators',
      author='giginet',
      author_email='giginet.net@gmail.com',
      url='https://github.com/giginet/ribbit',
      test_suite = "runtests.runtests",
      include_package_data = True,
      install_requires = [
        'PIL',
        'Django>=1.6.0',
        'factory_boy>=2.2.1',
        'easy-thumbnails',
        'honcho',
        'djangorestframework',
        'pulsar',
        'pyyaml'
      ],
      dependency_links = ['git+https://github.com/quantmind/pulsar.git@344a0f6ec78c09260d2f67b15ba434dec0914f57#egg=pulsar',]
)
