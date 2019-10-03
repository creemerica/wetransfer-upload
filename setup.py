from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wetransfer-upload',
    version='0.0.5',
    description='Upload files to WeTransfer',
    long_description=long_description,
    url='https://github.com/creemerica/wetransfer-upload',
    author='Spencer Cree',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords=['wetransfer', 'upload'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        "requests==2.20.0",
        "requests_toolbelt==0.4.0"
    ]
)