'''
Created on Oct 27, 2013

@author: SloevWarez
'''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' this class is used to receive osc messages as well as announce   '
' this service through zeroconf/bonjour                            '
' depends on the pyOsc and pyBnjour modules                        '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import time
import threading
import select
import random

import OSC
import pybonjour

class OscServer():
    def __init__(self,name,regType,address):
        self.name=name
        self.regType=regType
        self.address=address
        oscThreadTarget=self.initOscServer()
        
        self.oscThread = threading.Thread( target =  oscThreadTarget)
        self.oscThread.start()
        
        self.initBonjourServer()
    
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
    
    def register(self):
        def register_callback(sdRef, flags, errorCode, name, regType, domain):
            if errorCode == pybonjour.kDNSServiceErr_NoError:
                print 'Registered service:'
                print '  name    =', name
                print '  regtype =', regType
                print '  domain  =', domain
    
        sdRef = pybonjour.DNSServiceRegister(name = self.name,
                                                  regtype = self.regType,
                                                  port = self.port,
                                                  callBack = register_callback)    
        try:
            try:
                while self._isRegisterRunning:
                    ready = select.select([sdRef], [], [], self.timeout)
                    if sdRef in ready[0]:
                        pybonjour.DNSServiceProcessResult(sdRef)
            except Exception:
                print("exception in register")
                pass
        finally:
            sdRef.close()
            
    def run_register(self):
        """
        Run the Bonjour service registration
        """
        if not self._isRegisterRunning:
            self._isRegisterRunning = True
            self.register_t = threading.Thread(target=self.register)
#            self.register_t.setDaemon(daemon)
            self.register_t.start()

    def close(self):
        self.oscServer.close()
        print "Waiting for osc server-thread to finish"
        self.oscThread.join() 
        print "Waiting for bonjour server-thread to finish"
        self.sdRef.close()
        
    def printing_handler(self, addr, tags, stuff, source):
        print "---"
        print "received new osc msg from %s" % OSC.getUrlStr(source)
        print "with addr : %s" % addr
        print "typetags %s" % tags
        print "data %s" % stuff
        print "---"

        
def main():
    osc=OscServer("TestService", '_test._tcp','127.0.0.1')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        osc.close()

    

if __name__ == '__main__':    
    main()
