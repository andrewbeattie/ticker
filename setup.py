import os
from setuptools import setup, find_packages


def strip_comments(l):
    return l.split("#", 1)[0].strip()


def strip_version(l):
    return l.split("==", 1)[0].strip()


def get_requirements(fileName):
    return [
        req
        for req in (
            strip_version(strip_comments(line))
            for line in open(os.path.join(os.path.dirname(__file__), fileName)).readlines()
        )
        if req
    ]


install_requires = get_requirements("requirements.txt")

setup(
    name="ticker",
    version="1.0.0",
    entry_points={"console_scripts": ["ticker=tickspot.main:main"]},
    author="Andrew",
    description="Interact with TickSpot with Python",
    python_requires=">=3.6.8",
    packages=find_packages(),
    install_requires=install_requires,
)
