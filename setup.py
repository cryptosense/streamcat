from setuptools import find_packages, setup

setup(
    name='streamcat',
    packages=find_packages(exclude=('tests', 'docs')),
    version='0.1.1',
    description='Encode and decode concatenated objects as streams',
    long_description=open('README.rst', 'r').read(),
    author='Bertrand Bonnefoy-Claudet',
    author_email='bertrand@cryptosense.com',
    url='https://github.com/cryptosense/streamcat',
    download_url='https://github.com/cryptosense/streamcat/tarball/v0.1.1',
    keywords=['stream', 'file', 'json'],
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    install_requires=[],
)
