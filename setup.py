# -*- encoding: utf-8 -*-
import glob
import io
import re
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

from pip.req import parse_requirements


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


def get_install_reqs(req_file):
    [str(req_data.req) for req_data in parse_requirements(req_file, session=False)]


setup(
    name="lcmap-client",
    version="0.0.1",
    license="BSD",
    description="LCMAP REST Service Client (Python)",
    long_description="%s" % read("README.md"),
    author="USGS EROS",
    author_email="http://eros.usgs.gov",
    url="https://github.com/usgs-eros/lcmap-client-py",
    packages=find_packages("src"),
    package_dir={"": "src"},
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
    install_requires=get_install_reqs("requirements.txt"),
    extras_require={
        # eg: 'rst': ["docutils>=0.11"],
    },
    entry_points='''
        [console_scripts]
        lcmap=lcmap_client.scripts.cl_tool.main:main
    ''')
