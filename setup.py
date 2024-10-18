"""Setup for the the OTT Taxonomy package."""

import os
import re

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with open(os.path.join(here, "README.md"), encoding="utf8") as f:
    long_description = f.read()


def read(*parts):
    with open(os.path.join(here, *parts), "r", encoding="utf8") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


__version__ = find_version("ott_taxonomy", "__version__.py")

test_deps = [
    "pytest",
    "pytest-cov",
    "pytest-readme",
    "validate_version_code",
]

extras = {
    "test": test_deps,
}

setup(
    name="ott_taxonomy",
    version=__version__,
    description="Python package to interact with the OTT Taxonomy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    tests_require=test_deps,
    python_requires=">=3.12",
    include_package_data=True,
    install_requires=[
        "downloaders>=1.0.21",
        "setuptools>=75.2.0",
    ],
    extras_require=extras,
)
