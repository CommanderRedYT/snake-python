from setuptools import setup

setup(
    name='snake-python',
    version='1.0.0',
    description='A simple snake clone writen in python',
    url='https://github.com/CommanderRedYT/snake-python',
    author='CommanderRedYT',
    license='GPLv3',
    packages=['snake_python'],
    entry_points={
        'console_scripts': [
            'snake-python=snake_python.main:main',
        ],
    },
    python_requires='>=3.6',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[],
)
