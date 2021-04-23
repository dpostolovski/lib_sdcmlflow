from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [
    'mlflow',
    'google-api-python-client'
]

setup(
    name='sdc_mlflow',
    version='0.2',
    author='Damjan Postolovski',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    description='Tools for ML Ops.')
