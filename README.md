# python-healthcheckd

This program is intended to be used by a load balancer that can only understand HTTP codes as health status for backends

## configuration

```
[healthcheckd]

piddir = /tmp
pidfile = demo.pid
port = 9999
command = /bin/false
```
