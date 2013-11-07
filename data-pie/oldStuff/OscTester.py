import select
import socket
import sys
import pybonjour

class OscTest():
    def __init__(self):
        self.regtype  = '_test._tcp'
        self.timeout  = 5
        self.queried  = []
        self.resolved = []
        
        self.browse_sdRef = pybonjour.DNSServiceBrowse(regtype = self.regtype,
                                          callBack = self.browse_callback)
    def __call__(self):
        try:
            try:
                while True:
                    ready = select.select([self.browse_sdRef], [], [])
                    if self.browse_sdRef in ready[0]:
                        pybonjour.DNSServiceProcessResult(self.browse_sdRef)
            except KeyboardInterrupt:
                pass
        finally:
            self.browse_sdRef.close()
            
    def query_record_callback(self,sdRef, flags, interfaceIndex, errorCode, fullname,
                              rrtype, rrclass, rdata, ttl):
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            print '  IP         =', socket.inet_ntoa(rdata)
            self.queried.append(True)
    
    
    def resolve_callback(self,sdRef, flags, interfaceIndex, errorCode, fullname,
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
                                            callBack = self.query_record_callback)
    
        try:
            while not self.queried:
                ready = select.select([query_sdRef], [], [], self.timeout)
                if query_sdRef not in ready[0]:
                    print 'Query record timed out'
                    break
                pybonjour.DNSServiceProcessResult(query_sdRef)
            else:
                self.queried.pop()
        finally:
            query_sdRef.close()
    
        self.resolved.append(True)
    
    
    def browse_callback(self,sdRef, flags, interfaceIndex, errorCode, serviceName,
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
                                                    self.resolve_callback)
    
        try:
            while not self.resolved:
                ready = select.select([resolve_sdRef], [], [], self.timeout)
                if resolve_sdRef not in ready[0]:
                    print 'Resolve timed out'
                    break
                pybonjour.DNSServiceProcessResult(resolve_sdRef)
            else:
                self.resolved.pop()
        finally:
            resolve_sdRef.close()

def main():
    osctest=OscTest()

if __name__ == '__main__':    
    main()