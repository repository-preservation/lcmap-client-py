# -*- encoding: utf-8 -*-
import glob
import re
import io
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

def read(filename, codec='utf-8'):
    with io.open(filename, encoding=codec) as handle:
        return handle.read()

setup(
    name="lcmap-client",
    version="0.5.0",
    license="BSD",
    description="LCMAP REST Service Client (Python)",
    long_description="%s" % read("README.md"),
    author="USGS EROS",
    author_email="http://eros.usgs.gov",
    url="https://github.com/usgs-eros/lcmap-client-py",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages = ["lcmap"],

    # py_modules is an alternative way to look for what's included.
    # packages should handle it.  WIP
    py_modules=[splitext(basename(i))[0] for i in glob.glob("src/*.py")],

    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        #"Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
    keywords=[
        # eg: "keyword1", "keyword2", "keyword3",
    ],
    install_requires=['six', 'requests', 'pylru', 'termcolor', 'nose',
                      'click', 'DateTime', 'pygdal>=1.11.4,<=1.11.4.999',
                      'pandas'
    ],
    extras_require={
        'dev': ['nose', 'tox'],
        'test': ['nose', 'tox']
    },
    entry_points='''
        [console_scripts]
        lcmap=lcmap.client.scripts.cl_tool.main:main
    ''')
