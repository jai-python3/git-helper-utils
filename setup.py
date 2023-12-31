#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
     "Rich"
]

test_requirements = [ ]

setup(
    author="Jaideep Sundaram",
    author_email='jai.python3@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Collection of Python utility scripts to facilitate git related tasks.",
    entry_points={
        'console_scripts': [
            'create-git-branch=git_utils.create_git_branch:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='git_utils',
    name='git_utils',
    packages=find_packages(include=['git_utils', 'git_utils.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jai-python3/git_utils',
    version='0.1.0',
    zip_safe=False,
)