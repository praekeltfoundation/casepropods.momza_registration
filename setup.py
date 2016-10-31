import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    readme = f.read()

with open(os.path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(name='casepropods.momza_registration',
      version=version,
      description=('MomZA registrations data pod for casepro. Returns '
                   ' case specific registration information.'),
      long_description=readme,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Django",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Praekelt Foundation',
      author_email='dev@praekelt.com',
      url='http://github.com/praekeltfoundation/casepropods.momza_registration', # noqa
      license='BSD',
      keywords='',
      packages=['casepropods.momza_registration'],
      include_package_data=True,
      zip_safe=False,
      namespace_packages=['casepropods'],
      entry_points={})
