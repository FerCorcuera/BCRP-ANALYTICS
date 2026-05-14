from setuptools import find_packages, setup

setup(
    name="bcrp_analytics",
    version="0.1.0",
    description="Utilities for retrieving and analyzing BCRP data",
    author="Fernando Corcuera",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "requests",
    ],
)
