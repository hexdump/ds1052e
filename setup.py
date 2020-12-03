from setuptools import setup, find_packages

setup(
    name='ds1052e',
    version='1.0.4',
    author='Leslie Schumm',
    author_email='contact@hexdump.email',
    packages=['ds1052e'],
    install_requires=[
        'numpy',
        'python-usbtmc',
        'pyusb'
    ],
)
