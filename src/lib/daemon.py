#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

def daemonize():
    pid = os.fork()
    if pid != 0:
        os._exit(0)

    os.setsid()
    maxfd = os.sysconf("SC_OPEN_MAX")
    for fd in range(0, maxfd):
        try:
            os.close(fd)
        except OSError:
            pass
