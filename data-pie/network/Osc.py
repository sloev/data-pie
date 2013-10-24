
""" receiving OSC with pyOSC
https://trac.v2.nl/wiki/pyOSC
example by www.ixi-audio.net based on pyOSC documentation

this is a very basic example, for detailed info on pyOSC functionality check the OSC.py file 
or run pydoc pyOSC.py. you can also get the docs by opening a python shell and doing
>>> import OSC
>>> help(OSC)
"""


import OSC
import time, threading
import select
import sys
import pybonjour
import random
import threading
import exceptions

class OscServer():
    def __init__(self,name,regType,address):
        self.name=name
        self.regType=regType
        self.address=address
        oscThreadTarget=self.initOscServer()
        
        self.oscThread = threading.Thread( target =  oscThreadTarget)
        self.oscThread.start()
        
        self.bonjourThread = bonjourThread(self.name,self.regType,self.port)
        self.bonjourThread.start()
    
    def initOscServer(self):
        while True:
            try:
                self.port = 9000 + random.randint(0,999)
                self.oscServer = OSC.OSCServer((self.address, self.port))
                print "%s: got port %s" % (self.name, self.port)
                break
            except IOError:
                print "%s: didn't get port %s" % (self.name, self.port)
        self.oscServer.addDefaultHandlers()
        self.oscServer.addMsgHandler("/print", self.printing_handler) 
        return self.oscServer.serve_forever
        
    def close(self):
        self.oscServer.close()
        print "Waiting for osc server-thread to finish"
        self.oscThread.join() 
        print "Waiting for bonjour server-thread to finish"
        self.bonjourThread.stop()
        
    def printing_handler(self, addr, tags, stuff, source):
        print "---"
        print "received new osc msg from %s" % OSC.getUrlStr(source)
        print "with addr : %s" % addr
        print "typetags %s" % tags
        print "data %s" % stuff
        print "---"
    
class bonjourThread(threading.Thread):

    def __init__(self,name,regType,port):
        threading.Thread.__init__(self)
        self.finished = threading.Event()

        def register_callback(sdRef, flags, errorCode, name, regType, domain):
            if errorCode == pybonjour.kDNSServiceErr_NoError:
                print 'Registered service:'
                print '  name    =', name
                print '  regtype =', regType
                print '  domain  =', domain
    
        self.sdRef = pybonjour.DNSServiceRegister(name = name,
                                                  regtype = regType,
                                                  port = port,
                                                  callBack = register_callback)        
    def run(self):
        while not self.finished.isSet():
            print("running")
            try:
                ready = select.select([self.sdRef], [], [])
                if self.sdRef in ready[0]:
                    pybonjour.DNSServiceProcessResult(self.sdRef)
            except Exception as ex:
                print("troll\n\n"+ex)
        print("end")
#         print "a"
#         print "b"
#         self.join()

    def stop (self):
        self.finished.set()
        self.sdRef.close()
        self.join()

        print("lol")

        
def main():
    osc=OscServer("TestService", '_test._tcp','127.0.0.1')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        osc.close()

    

if __name__ == '__main__':    
    main()
