#!/usr/bin/env python

import subprocess
import threading
import time

class Pinger(object):
    hosts = []
    status = { 'alive' : [], 'dead' : []}

    thread_count = 4
    retry = 5
    interval = 1
    lock = threading.Lock()

    def ping(self, ip):
        ret = subprocess.call(['ping', '-c', '1', '-W', '1', ip],
                                stdout=open('/dev/null','w'), stderr=open('/dev/null','w'))

        for i in range(1, self.retry):
            if ret ==0:
                break
            time.sleep(self.interval)
            ret = subprocess.call(['ping', '-c', '1', '-W', '1', ip],
                                stdout=open('/dev/null','w'), stderr=open('/dev/null','w'))

        return ret == 0

    def pop_queue(self):
        ip = None
        self.lock.acquire()

        if self.hosts:
            ip = self.hosts.pop()

        self.lock.release()

        return ip

    def dequeue(self):
        while True:
            ip = self.pop_queue()

            if not ip:
                return None

            result = 'alive' if self.ping(ip) else 'dead'

            self.status[result].append(ip)

    def start(self):
        threads = []

        for i in range(self.thread_count):

            t = threading.Thread(target=self.dequeue)
            t.start()
            threads.append(t)

        [ t.join() for t in threads ]

        return self.status

if __name__ == '__main__':
    ping = Pinger()

    ping.hosts = [
        '8.8.8.8' , '10.161.133.1' , '10.161.211.201' , '10.161.211.202' , '10.161.211.203' , '10.161.211.204' , '10.161.211.205' ]
    print ping.start()
