# pylint: disable=missing-docstring
from setuptools import setup


setup(
    name='pyscc',
    description='py-component-controller is an opinionated framework for structuring selenium test suites. This project depends on the pyselenium-js project.',
    version='0.1.7',
    url='https://neetjn.github.io/py-component-controller/',
    author='John Nolette',
    author_email='john@neetgroup.net',
    license='Apache2',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
    ],
    install_requires=[
        'selenium==3.6.0',
        'pyseleniumjs==1.3.7',
        'six'
    ],
    packages=['pyscc']
)
