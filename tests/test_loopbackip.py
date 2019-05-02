#!/usr/bin/env python3

from pyroute2 import IPDB
from loopbackip import update_loopback_ips
import pytest
import json
from operator import itemgetter
from os import environ

if environ.get('PYDEV_IP'):
    import pydevd_pycharm


@pytest.fixture(scope='module')
def loopback_interface():
    with IPDB() as ipdb:
        yield ipdb.interfaces['lo']


@pytest.fixture(autouse=True)
def flush_loopback_ips():
    update_loopback_ips([])


@pytest.fixture(scope='module')
def load_ips():
    with open('/tests/loopback_ips.json') as f:
        return json.load(f)


@pytest.mark.parametrize('indices',
                         [pytest.param([0], id='empty_list'),
                          pytest.param([1], id='add_ip'),
                          pytest.param([1, 3], id='add_second_ip'),
                          pytest.param([3, 1], id='remove_ip'),
                          pytest.param([1, 2], id='replace_ip'),
                          pytest.param([4], id='invalid_config', marks=pytest.mark.xfail)
                          ])
def test_update_loopback_ips(loopback_interface, load_ips, indices):
    if environ.get('PYDEV_IP'):
        pydevd_pycharm.settrace(environ.get('PYDEV_IP'), port=int(environ.get('PYDEV_PORT')),
                                stdoutToServer=True, stderrToServer=True)
    def cast_to_tuple(items):
        return items if isinstance(items, tuple) else (items, )
    for ips in cast_to_tuple(itemgetter(*indices)(load_ips)):
        update_loopback_ips(ips)
        assert sorted(ips) == sorted(addr[0] for addr in loopback_interface.ipaddr if addr[0] != '127.0.0.1')
