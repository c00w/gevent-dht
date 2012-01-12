#!/usr/bin/env python

from setuptools import setup
setup(name='gevent_dht',
        version='0.1.2',
        description='Gevent based distributed hash table',
        author='Colin Rice',
        author_email='dah4k0r@gmail.com',
        packages = ['gevent_dht'],
        url='github.com/c00w/gevent_dht',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: System :: Networking',
            'License :: OSI Approved :: MIT License',
            ],
        install_requires= 'gevent',
        license = 'MIT Expat License'
        )
