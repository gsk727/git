import os
import sys

pid = os.fork()
from threading import Lock
l = Lock()

i = 0
if pid == 0:
    l.acquire()
    print "child"
else:
    l.acquire()
    l.acquire()
    print "parent"

