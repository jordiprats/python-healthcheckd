# python-healthcheckd

This program is intended to be used by a load balancer that can only understand HTTP codes as health status for backends

If the command returns 0 it will answer with a HTTP/200, otherwise it will be an HTTP/503

## configuration

```
[healthcheckd]

piddir = /tmp
pidfile = demo.pid
port = 9999
command = /bin/false
```
