'''
Created on Nov 6, 2013

@author: johannes
'''
import select
import sys
import pybonjour
import socket
import time
import threading

class Bonjour():
    def __init__(self,name,regtype,port):
        self.name=name
        self.regtype=regtype
        self.port=port
        
        self.browserQueried  = []
        self.browserResolved = []
        
        self.browserLock=threading.Lock()
        self.timeout  = 5

        self.registerStopEvent = threading.Event()
        self.browserStopEvent = threading.Event()
        
        self.clients = dict()
        
        pass
    
    def runRegister(self):
        self.registerStopEvent.clear()
        self.registerThread=threading.Thread(target=self.register)
        self.registerThread.start()
        
    def stopRegister(self):
        self.registerStopEvent.set()
        self.registerThread.join()

    def runBrowser(self):
        self.browserStopEvent.clear()
        self.browserThread=threading.Thread(target=self.browser)
        self.browserThread.start()
        
    def stopBrowser(self):
        self.browserStopEvent.set()
        self.browserThread.join()
    
    def register(self):
        def register_callback(sdRef, flags, errorCode, name, regtype, domain):
            if errorCode == pybonjour.kDNSServiceErr_NoError:
                print 'Registered service:'
                print '  name    =', name
                print '  regtype =', regtype
                print '  domain  =', domain
        
        
        sdRef = pybonjour.DNSServiceRegister(name = self.name,
                                             regtype = self.regtype,
                                             port = self.port,
                                             callBack = register_callback)
        
        try:
            while not self.registerStopEvent.is_set():
                ready = select.select([sdRef], [], [],self.timeout*2)
                if sdRef in ready[0]:
                    pybonjour.DNSServiceProcessResult(sdRef)
#                self.regStopEvent.wait(0.01)
        finally:
            sdRef.close()
        print("exiting register thread")
        
    def browser(self):
        def query_record_callback(sdRef, flags, interfaceIndex, errorCode, fullname,
                                  rrtype, rrclass, rdata, ttl):
            if errorCode == pybonjour.kDNSServiceErr_NoError:
                print '  IP         =', socket.inet_ntoa(rdata)
                print("fullname="+str(fullname))
                self.browserQueried.append(True)
        
        
        def resolve_callback(sdRef, flags, interfaceIndex, errorCode, fullname,
                             hosttarget, port, txtRecord):
            if errorCode != pybonjour.kDNSServiceErr_NoError:
                return
        
            print 'Resolved service:'
            print '  fullname   =', fullname
            print '  hosttarget =', hosttarget
            print '  port       =', port
        
            query_sdRef = \
                pybonjour.DNSServiceQueryRecord(interfaceIndex = interfaceIndex,
                                                fullname = hosttarget,
                                                rrtype = pybonjour.kDNSServiceType_A,
                                                callBack = query_record_callback)
        
            try:
                while not self.browserQueried:
                    ready = select.select([query_sdRef], [], [], self.timeout)
                    if query_sdRef not in ready[0]:
                        print 'Query record timed out'
                        break
                    pybonjour.DNSServiceProcessResult(query_sdRef)
                else:
                    self.browserQueried.pop()
            finally:
                query_sdRef.close()
        
            self.browserResolved.append(True)
            print(str(self.browserResolved))
        
        
        def browse_callback(sdRef, flags, interfaceIndex, errorCode, serviceName,
                            regtype, replyDomain):
            if errorCode != pybonjour.kDNSServiceErr_NoError:
                return
        
            if not (flags & pybonjour.kDNSServiceFlagsAdd):
                print 'Service removed'
                return
        
            print 'Service added; resolving'
        
            resolve_sdRef = pybonjour.DNSServiceResolve(0,
                                                        interfaceIndex,
                                                        serviceName,
                                                        regtype,
                                                        replyDomain,
                                                        resolve_callback)
            try:
                while not self.browserResolved:
                    ready = select.select([resolve_sdRef], [], [], self.timeout)
                    if resolve_sdRef not in ready[0]:
                        print 'Resolve timed out'
                        break
                    pybonjour.DNSServiceProcessResult(resolve_sdRef)
                else:
                    self.browserResolved.pop()
            finally:
                resolve_sdRef.close()
        
        
        browse_sdRef = pybonjour.DNSServiceBrowse(regtype = self.regtype,
                                                  callBack = browse_callback)
        
        try:
            while not self.browserStopEvent.is_set():
                ready = select.select([browse_sdRef], [], [],self.timeout*2)
                if browse_sdRef in ready[0]:
                    pybonjour.DNSServiceProcessResult(browse_sdRef)
        finally:
            browse_sdRef.close()
        print("exiting browser thread")
        

def main():
    name="TestService"
    port=9027
    regtype='_test._tcp'
    
    a=Bonjour(name,regtype,port)
    b=Bonjour(name,regtype,port)
    
    a.runRegister()
    time.sleep(2)
    b.runBrowser()
    
    time.sleep(7)
    print("stopping register")
    a.stopRegister()
    time.sleep(10)
    print("stopping browser")
    b.stopBrowser()
    print("exiting")
    
if __name__ == '__main__':
    main()



