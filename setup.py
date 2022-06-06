from setuptools import find_packages, setup
from data_product_service import __version__

setup(
    name="data_product_service",
    packages=find_packages(exclude=["tests", "tests.*"]),
    setup_requires=["wheel"],
    version=__version__,
    description="DBX SQL Endpoint",
    author="Gaurav Malhotra",
)
