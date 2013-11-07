import threading
import time

class Lol():
    def __init__(self):
        self.t1Event=threading.Event()
        self.t2Event=threading.Event()
        
        self.t1=threading.Thread(target=self.thread1)
        self.t2=threading.Thread(target=self.thread2)
        
        self.lock=threading.Lock()
        self.tmp=1
        self.t1.start()
        self.t2.start()
    
    def thread1(self):
        while(not self.t1Event.is_set()):
            self.lock.acquire()
            try:
                self.tmp=self.tmp+1
                print("t1 tmp="+str(self.tmp))
            finally:
                self.lock.release()
            print("t1 running")
            self.t1Event.wait(1)
            pass
        print("t1 leave")
    
    def stopThreads(self):
        self.t1Event.set()
        self.t2Event.set()
        
    def thread2(self):
        while(not self.t2Event.is_set()):
            self.lock.acquire()
            try:
                self.tmp=self.tmp+1
                print("t2 tmp="+str(self.tmp))
            finally:
                self.lock.release()
            print("t2 running")
            self.t2Event.wait(1.1)
            pass
        print("t2 leave")
        
def main():
    lol=Lol()
    time.sleep(5)
    lol.stopThreads()

if __name__ == '__main__':
    main()

