#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

readme = open('README').read()

long_description = """
This is a CLI tool for interacting with Amazon's ELB.
----

%s

----
For more information, run ``elb_tool -h``.
""" % (readme)

config = {
    'description': 'elb_tool',
    'author': 'Rob Terhaar',
    'author_email': 'rterhaar@atlanticdynamic.com',
    'license': 'BSD',
    'url': '.',
    'download_url': '.',
    'version': '0.1',
    'install_requires': ['nose','boto','argparse'],
    'packages': ['elb_tool'],
    'scripts': ['bin/elb_tool'],
    'name': 'elb_tool'
}

setup(**config)
