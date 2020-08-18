#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['seaborn>=0.10', 'scipy>=1.5', 'numpy>=1.19', 'matplotlib>=3.2', 'pandas>=1.0', 'adjustText>=0.7']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Peter C DeWeirdt",
    author_email='petedeweirdt@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Plotting functions for the Genetic Perturbation Platform's R&D group at the Broad institute.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='gpplot',
    name='gpplot',
    packages=find_packages(include=['gpplot', 'gpplot.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/gpp-rnd/gpplot',
    version='0.5.0',
    zip_safe=False,
)
