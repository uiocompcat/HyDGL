from setuptools import setup
import versioneer

requirements = [
    # package requirements go here
]

setup(
    name='nbo2graph',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Python parser to generate descriptive graphs from Natural Bond Orbitals (NBO).",
    license="MIT",
    author="Hannes Kneiding",
    author_email='hanneskn@uio.no',
    url='https://github.com/hkneiding/nbo2graph',
    packages=['nbo2graph'],
    entry_points={
        'console_scripts': [
            'nbo2graph=nbo2graph.cli:cli'
        ]
    },
    install_requires=requirements,
    keywords='nbo2graph',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
