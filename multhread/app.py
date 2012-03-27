#-*-coding:utf-8 -*-
from flask import Flask
import time

from threading import Lock
import threading
import pymongo

db = pymongo.Connection().app
#g_lock = Lock()

app = Flask(__name__)

@app.route("/test", methods=["GET",])
def test():
    print "\n\n======================================"
    t = threading.currentThread()
    print t.getName(), t.ident
    res = db.test.test.find_one({"name":1})
    if res:
        return "hello world"
    time.sleep(10)
    db.test.test.insert({"name":1})

    return "insert"

if __name__ == "__main__":
    app.run(debug=True)

    
