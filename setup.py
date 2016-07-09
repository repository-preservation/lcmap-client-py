# -*- encoding: utf-8 -*-
import glob
import re
import io
import sys
from sys import version_info
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
        #import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)

def read(filename, codec=None):
    with io.open(filename, mode='rb', encoding=codec) as handle:
        return handle.read()


def min_gdal_version():
    ''' Returns the installed gdal version or Exception if not installed '''

    cmd = ['gdal-config', '--version']

    if version_info >= (2,4) and version_info <= (2,6):
        from subprocess import Popen, PIPE
        p = Popen(cmd, stdout=PIPE)
        version = p.communicate()[0].strip()
    elif version_info >=(2,7):
        from subprocess import check_output
        version = check_output(cmd).strip()
    else:
        raise Exception('Unsupported Python version:{0}.{1}.{2}'
            .format(version_info.major,
                    version_info.minor,
                    version_info.micro))

    if (type(version) is not str):
        version = version.decode('utf-8')

    return version


def max_gdal_version():
    ''' Returns the maximum pygdal version that can be installed '''
    #parts = min_gdal_version().decode('utf-8').split('.')
    parts = min_gdal_version().split('.')
    if len(parts) == 3:
        parts.append('999')
        max_version = '.'.join(parts)
    elif len(parts) > 3:
        max_version = '.'.join(parts)
    else:
        raise Exception('Can\'t determine max gdal version from {0}'
            .format(min_gdal_version()))

    if (type(max_version) is not str):
        max_version = max_version.decode('utf-8')

    return max_version


setup(
    name='lcmap-client',
    version='0.5.0',
    license='NASA Open Source Agreement 1.3',
    description='LCMAP REST Service Client (Python)',
    long_description='{0}'.format(read('README.md')),
    author='USGS EROS',
    author_email='http://eros.usgs.gov',
    url='https://github.com/usgs-eros/lcmap-client-py',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages = ['lcmap'],

    # py_modules is an alternative way to look for what's included.
    # packages should handle it.  WIP
    py_modules=[splitext(basename(i))[0] for i in glob.glob('src/*.py')],

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
    keywords=[
        # eg: "keyword1", "keyword2", "keyword3",
    ],
    install_requires=['six', 'requests', 'pylru', 'termcolor', 'nose',
                      'click', 'DateTime',
                      'pygdal>={0},<={1}'.format(min_gdal_version(),
                                                 max_gdal_version()),
                      'pandas'
    ],
    tests_require=['tox'],
    cmdclass = {'test': Tox},
    extras_require={
        'dev': [''],
        'test': ['']
    },
    entry_points= {
        'console_scripts': [
        'lcmap=lcmap.client.scripts.cl_tool.main:main']
    },
)
