"""Setup script for devcontext."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="devcontext",
    version="0.1.0",
    author="jhony91792-oss",
    author_email="jhony91792@gmail.com",
    description="CLI that creates AI-ready context from your codebase",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhony91792-oss/devcontext",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "devcontext=devcontext.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)