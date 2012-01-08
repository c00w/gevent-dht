#!/bin/bash

nosetests ./gevent_dht/*.py
sudo python setup.py install
