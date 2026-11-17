from setuptools import setup, find_packages

setup(
    name="job_finder",
    version="0.2",
    packages=find_packages(include=["etl", "etl.*"]),
)
