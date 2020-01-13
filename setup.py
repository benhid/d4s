from os.path import abspath, dirname, join

from setuptools import find_packages, setup

basedir = abspath(dirname(__file__))

with open(join(basedir, 'README.md'), encoding='utf-8') as f:
    README = f.read()


setup(
    name='d4s',
    version='0.0.1',
    description='Data4Science Python client',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Antonio Benitez-Hidalgo',
    author_email='antonio.benitez@lcc.uma.es',
    license='MIT',
    url='https://github.com/benhid/d4s',
    packages=find_packages(exclude=['test_']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    install_requires=['requests', 'cached_property']
)
