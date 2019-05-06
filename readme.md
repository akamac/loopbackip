### Docker image to assign ip addresses from file on loopback interface

Send `SIGHUP` to read ip from `/loopback_ip.txt` (one per line) and assign to loopback interface.
Needs to be run with `--cap-add NET_ADMIN` and `--sysctl`.

```yaml
sysctls:
  net.ipv4.conf.lo.arp_announce: 2
  net.ipv4.conf.lo.arp_ignore: 3
```

### Run unit tests

```bash
docker build -t intermedia/loopbackip . && docker build -t loopbackip:pytest tests
docker run --cap-add=NET_ADMIN loopbackip:pytest
# remote interactive debug with pyvdev 
docker run --rm --cap-add=NET_ADMIN -e PYDEV_IP=10.9.3.185 -e PYDEV_PORT=4444 loopbackip:pytest
```