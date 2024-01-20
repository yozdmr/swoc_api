from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A package that pulls boys/girls soccer data swocsports.com'

# Setting up
setup(
    name="swocstats",
    version=VERSION,
    author="Yusuf Ozdemir",
    author_email="<ozdemiye@miamioh.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=['beautifulsoup4', 'requests'],
    keywords=['sports data', 'south west ohio conference', 'swoc', 'soccer data'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: Under Development",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ]
)