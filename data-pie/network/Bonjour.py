'''
Created on Oct 20, 2013

@author: johannes
'''

import time
import select
import sys
import pybonjour

class Bonjour():
    def __init__(self,name,regtype,port):
        def register_callback(sdRef, flags, errorCode, name, regtype, domain):
            if errorCode == pybonjour.kDNSServiceErr_NoError:
                print 'Registered service:'
                print '  name    =', name
                print '  regtype =', regtype
                print '  domain  =', domain
                
        self.sdRef = pybonjour.DNSServiceRegister(name = name,
                                     regtype = regtype,
                                     port = port,
                                     callBack = register_callback)
        ready = select.select([self.sdRef], [], [])
        if self.sdRef in ready[0]:
            pybonjour.DNSServiceProcessResult(self.sdRef)

    def close(self):
        self.sdRef.close()
   
def main():
    bonjour=Bonjour("TestService", '_test._tcp', 1234) 
    time.sleep(20)
    bonjour.close()
    
if __name__ == '__main__':
    main()
