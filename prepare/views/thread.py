from threading import Thread

class T(Thread):
    def __init__(self, target = None):
            Thread.__init__(self, target)
            self.start()
            self.join()



