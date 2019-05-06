#!/usr/bin/env python3

import signal
from pyroute2 import IPDB


def read_ips():
    print('Loading ip address(-es) from config')
    with open('/config/loopback_ip.txt') as f:
        return f.readlines()


def update_loopback_ips(ips):
    print('Updating loopback ip addresses')
    ips = set(ips)
    ips.add('127.0.0.1')
    with IPDB() as ipdb:
        with ipdb.interfaces['lo'] as lo:
            for addr in lo.ipaddr:
                if addr[0] not in ips:
                    lo.del_ip(addr[0], 32)
            for ip in ips:
                if ip not in [addr[0] for addr in lo.ipaddr]:
                    try:
                        lo.add_ip(ip, 32, scope=254) # RT_SCOPE_HOST
                    except:
                        print('Cannot add {}'.format(ip))


def flush_n_exit():
    print('Received termination request. Flushing loopback ip addresses')
    update_loopback_ips([])
    raise SystemExit


def main():
    update_loopback_ips(read_ips())

    signal.signal(signal.SIGHUP, lambda s, f: update_loopback_ips(read_ips()))
    signal.signal(signal.SIGINT, lambda s, f: flush_n_exit())  # Nomad
    signal.signal(signal.SIGTERM, lambda s, f: flush_n_exit())  # Docker
    while True:
        print('Waiting for SIGHUP to reload loopback config')
        signal.pause()


if __name__ == '__main__':
    main()
