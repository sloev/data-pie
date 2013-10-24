'''
Created on Oct 23, 2013

@author: johannes
'''
import select
import sys
import pybonjour
import OSC
import socket
import time, random


regtype  = '_osc._udp'
timeout  = 5
queried  = []
resolved = []
c = OSC.OSCClient()
ip=''
port=0


def query_record_callback(sdRef, flags, interfaceIndex, errorCode, fullname,
                          rrtype, rrclass, rdata, ttl):
    if errorCode == pybonjour.kDNSServiceErr_NoError:
        ip=socket.inet_ntoa(rdata)
        print '  IP         =', socket.inet_ntoa(rdata)
        queried.append(True)


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
        while not queried:
            ready = select.select([query_sdRef], [], [], timeout)
            if query_sdRef not in ready[0]:
                print 'Query record timed out'
                break
            pybonjour.DNSServiceProcessResult(query_sdRef)
        else:
            queried.pop()
    finally:
        query_sdRef.close()

    resolved.append(True)


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
        while not resolved:
            ready = select.select([resolve_sdRef], [], [], timeout)
            if resolve_sdRef not in ready[0]:
                print 'Resolve timed out'
                break
            pybonjour.DNSServiceProcessResult(resolve_sdRef)
        else:
            resolved.pop()
    finally:
        resolve_sdRef.close()


browse_sdRef = pybonjour.DNSServiceBrowse(regtype = regtype,
                                          callBack = browse_callback)

try:
    try:
        ready = select.select([browse_sdRef], [], [])
        if browse_sdRef in ready[0]:
            pybonjour.DNSServiceProcessResult(browse_sdRef)
        seed = random.Random() # need to seed first 

        while True:
            if(c.address() not in None):
                rNum= OSC.OSCMessage()
                rNum.setAddress("/print")
                n = seed.randint(1, 1000) # get a random num every loop
                rNum.append(n)
                c.send(rNum)
                time.sleep(5) # wait here some secs


                print
    except KeyboardInterrupt:
        pass
finally:
    browse_sdRef.close()

