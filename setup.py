import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

desc = "A project generator tools for easy create project skeleton."

try:
	long_description = read('ansprogen/README.md')
except:
	long_description = desc

setup(
    name = "ansprogen",
    version = "0.0.5",
    author = "Robin Syihab",
    author_email = "r[@]nosql.asia",
    description = (desc),
    license = "MIT",
    keywords = "ansprogen project generator",
    url = "http://www.mindtalk.com/u/anvie",
	download_url = "https://github.com/anvie/Ansprogen",
    packages=find_packages(),
	package_data = {
		'': ['README.md', '*.py']
	},
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
	entry_points='''
	[console_scripts]
	progen = ansprogen.progen:main
	'''
)
