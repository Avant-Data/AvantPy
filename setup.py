from setuptools import find_packages, setup
setup(
    name='avantpy',
    packages=find_packages(include=['avantpy']),
    version='0.1.0',
    description='Avant Data Python Library',
    long_description=open('README.md').read(),
    author='AvantData',
    #license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)