try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'elb_tool',
    'author': 'Rob Terhaar',
    'url': '.',
    'download_url': '.',
    'version': '0.1',
    'install_requires': ['nose','boto','argparse'],
    'packages': ['elb_tool'],
    'scripts': [],
    'name': 'elb_tool'
}

setup(**config)
