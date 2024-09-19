from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()
if not requirements:
    requirements = []

setup(
    name='eval_data',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=requirements,
)
