# -*- encoding: utf-8 -*-
import glob
import io
import sys
from os.path import basename
from os.path import splitext
from setuptools import find_packages
from setuptools import setup
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


def read(filename, codec=None):
    with io.open(filename, mode='rb', encoding=codec) as handle:
        return handle.read()


setup(
    name='lcmap-client',
    version='1.0.0-dev',
    license='NASA Open Source Agreement 1.3',
    description='LCMAP REST Service Client (Python)',
    long_description='{0}'.format(read('README.md')),
    author='USGS EROS',
    author_email='custserv@usgs.gov',
    url='https://github.com/usgs-eros/lcmap-client-py',
    packages=find_packages('lcmap_client'),
    package_dir={'': 'lcmap_client'},
    namespace_packages=['lcmap'],

    # py_modules is an alternative way to look for what's included.
    # packages should handle it.  WIP
    py_modules=[splitext(basename(i))[0] for i in glob.glob('lcmap_client/*.py')],

    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    keywords=['lcmap', 'landsat', 'remote sensing'],
    install_requires=['six', 'requests', 'pylru', 'termcolor', 'nose', 'click', 'DateTime', 'pandas'],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    extras_require={
        'dev': [''],
        'test': ['']
    },
    entry_points={
        'console_scripts': ['lcmap=lcmap.client.scripts.cl_tool.main:main']
    },
)
