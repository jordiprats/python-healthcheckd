# python-healthcheckd

This program is intended to be used by a load balancer that can only understand HTTP codes as health status for backends

If the command returns 0 it will answer with a HTTP/200, otherwise it will be an HTTP/503

## usage

Global healthcheckd section:
* **piddir**: PID directory where to store pidfiles
* **pidfile**: PID filename
* **port**: Port to listen to
* **command**: Command to execute to check for health status

## configuration

```
[healthcheckd]

piddir = /tmp
pidfile = demo.pid
port = 9999
command = /bin/false
```
