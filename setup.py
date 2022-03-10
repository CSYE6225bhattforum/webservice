import pathlib

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='webservice',
    version='0.0.1',
    description='A very basic webservice',
    long_description=long_description,
    author='Forum Bhatt',
    author_email='bhatt.f@northeastern.edu',
    packages=find_packages(),
    install_requires=[
        'flask', 
        'pytest', 
        'bcrypt',
        'flask_sqlalchemy', 
        'psycopg2-binary'
    ]
)