from pathlib import Path

from setuptools import find_packages
from setuptools import setup

setup(
    name="peanocode",
    packages=find_packages(exclude=["tests"]),
    url="https://github.com/petaflot/peanocode",
    license="GPLv3",
    author=("kobauman","JCZD"),
    author_email=(None,"jczd@engrenage.ch"),
    description=(
        "Peanocode is a Python library for encoding Peano curves, calculating square-to-linear ratio and searching for a minimal curve based on the specified first step and fractal genius."
    ),
    long_description=Path("README.md").read_text(),
    classifiers=[
        "Development Status :: 1 - Prototype",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GPLv3 License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        #"Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={"console_scripts": ["bytestrings = peanocode.peanocode:main"]},
    setup_requires=["setuptools_scm"],
    #extras_require={"images": ["pillow"]},
    include_package_data=True,
)
