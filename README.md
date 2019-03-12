# python-healthcheckd

This program is intended to be used by a load balancer that can only understand HTTP codes a health status

## configuration

```
[healthcheckd]

piddir = /tmp
pidfile = demo.pid
port = 9999
command = /bin/false
```
