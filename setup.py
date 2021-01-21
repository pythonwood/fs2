#!/usr/bin/env python

# doc: https://packaging.python.org/tutorials/packaging-projects/
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository testpypi dist/fscmd-0.0.2*
# python3 -m pip install --index-url https://test.pypi.org/simple/ fscmd==0.0.2

from setuptools import setup, find_packages

with open("fscmd/_version.py") as f:
    exec(f.read())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: System :: Filesystems",
]

REQUIREMENTS = ["setuptools", "click", 'fs']

# CONSOLE_SCRIPTS = ['fscmd = fscmd.fscmd:fscmd'] # failed
CONSOLE_SCRIPTS_STR = '''
        [console_scripts]
        fscmd=fscmd:fscmd
    '''

setup(
    author="pythonwood",
    author_email="58223837@qq.com",
    # classifiers=CLASSIFIERS,
    description="A cmd tool based on pyfilesystem2 lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=REQUIREMENTS,
    extras_require={
        ":python_version < '3.6'": ["typing~=3.6"],
    },
    license="MIT",
    name="fscmd",
    packages=find_packages(exclude=("tests",)),
    package_data={"fs": ["py.typed"]},
    zip_safe=False,
    platforms=["any"],
    url="https://github.com/pythonwood/fscmd",
    version=__version__,
    # entry_points={"console_scripts": CONSOLE_SCRIPTS}, # failed
    # scripts=['fscmd'],
    entry_points=CONSOLE_SCRIPTS_STR,
    python_requires='>=3.6',
)
