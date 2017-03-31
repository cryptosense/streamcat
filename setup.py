from setuptools import find_packages, setup

setup(
    name='streamcat',
    packages=find_packages(exclude=('tests', 'docs')),
    description='Deal with concatenated objects in a stream-like fashion',
    long_description=open('README.rst', 'r').read(),
    author='Bertrand Bonnefoy-Claudet',
    author_email='bertrand@cryptosense.com',
    url='https://github.com/cryptosense/streamcat',
    keywords=['stream', 'file', 'json'],
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    install_requires=[],
)
