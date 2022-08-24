from setuptools import setup, find_packages
from nbo2graph import __version__

setup(
    name='nbo2graph',
    version=__version__,

    url='https://github.com/hkneiding/nbo2graph',
    author='Hannes Kneiding',
    author_email='hannes.kneiding@outlook.com',
    packages=find_packages(exclude=['test'])
)
