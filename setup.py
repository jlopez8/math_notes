#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
]

setup_requirements = []

test_requirements = []

setup(
    author="Jaime Lopez-Merizalde",
    author_email="jaime.meriz13@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="math_notes is a tool that integrates anatural"
    + "handwritten math with digital notetaking means"
    + "in an online environment.t making the accessible"
    + "anywhere and easy to transition"
    + "from work or home.",
    entry_points={
        "console_scripts": [
            "math_notes=math_notes.cli:main",
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="math_notes",
    name="math_notes",
    packages=find_packages(include=["math_notes", "math_notes.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/jlopez8/math_notes",
    version="0.1.0",
    zip_safe=False,
)
