from setuptools import setup, find_packages
from HyDGL import __version__

setup(
    name='HyDGL',
    version=__version__,

    url='https://github.com/hkneiding/HyDGL',
    author='Hannes Kneiding',
    author_email='hannes.kneiding@outlook.com',
    packages=find_packages(exclude=['test'])
)
