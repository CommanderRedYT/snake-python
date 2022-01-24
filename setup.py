from setuptools import setup

setup(
    name='snake-python',
    version='1.2.0',
    description='A simple snake clone writen in python',
    url='https://github.com/CommanderRedYT/snake-python',
    author='CommanderRedYT',
    license='GPLv3',
    packages=['snake_python'],
    entry_points={
        'console_scripts': [
            'snake-python=snake_python.main:main',
            'snake-python-server=snake_python.server:server',
        ],
    },
    python_requires='>=3.6',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'pygame>=2.1.2',
        'pygame-menu>=4.2.2',
        'argparse>=1.4.0',
        'simple-websocket-server>=0.4.1',
        'dnspython>=2.2.0',
        'websocket-client>=1.2.3',
        'rel>=0.4.7',
        'asyncio>=3.4.3',
        'websockets>=10.1',
    ],
)
