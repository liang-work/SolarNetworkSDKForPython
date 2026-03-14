"""
Setup script for Solar Network Python SDK.

This script sets up the package for distribution.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    """Read the README file."""
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements from requirements.txt if it exists
def read_requirements():
    """Read requirements from requirements.txt."""
    requirements_file = "requirements.txt"
    if os.path.exists(requirements_file):
        with open(requirements_file, "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    return []

setup(
    name="solar-network-sdk",
    version="1.0.0",
    author="nanci",
    author_email="admin@thsl.dpdns.org",
    description="A Python SDK for interacting with the Solar Network API(Not official)",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/solarnetwork/python-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
    },
    include_package_data=True,
    package_data={
        "solar_network_sdk": ["py.typed"],
    },
    zip_safe=False,
    keywords="solar network api sdk authentication",
    project_urls={
        "Bug Reports": "https://github.com/solarnetwork/python-sdk/issues",
        "Source": "https://github.com/solarnetwork/python-sdk",
    },
)