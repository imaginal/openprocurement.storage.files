from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

version = '1.0.1'

requires = [
    'openprocurement.documentservice',
    'python-magic',
    'pytz',
    'requests',
    'rfc6266',
    'setuptools',
    'simplejson'
]
test_requires = requires + [
    'webtest',
    'python-coveralls',
]
docs_requires = requires + [
    'sphinxcontrib-httpdomain',
]
entry_points = {
    'openprocurement.documentservice.plugins': [
        'files = openprocurement.storage.files:includeme'
    ]
}

setup(name='openprocurement.storage.files',
      version=version,
      description="Simple Files storage for OpenProcurement document service",
      long_description=README,
      classifiers=[
          "Framework :: Pylons",
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
      ],
      keywords='web services',
      author='Volodymyr Flonts',
      author_email='vflonts@gmail.com',
      url='https://github.com/openprocurement/openprocurement.storage.files',
      license='Apache License 2.0',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['openprocurement', 'openprocurement.storage'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=test_requires,
      extras_require={'test': test_requires, 'docs': docs_requires},
      test_suite="openprocurement.storage.files.tests.main.suite",
      entry_points=entry_points)
