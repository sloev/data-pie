'''
Created on Oct 23, 2013

@author: johannes
'''
import select
import sys
import pybonjour
import OSC
import time, random

regtype  = '_osc._udp'
timeout  = 5
resolved = []

# OSC basic client
c = OSC.OSCClient()

def resolve_callback(sdRef, flags, interfaceIndex, errorCode, fullname,
                     hosttarget, port, txtRecord):
    if errorCode == pybonjour.kDNSServiceErr_NoError:
        print 'Resolved service:'
        print '  fullname   =', fullname
        print '  hosttarget =', hosttarget
        print '  port       =', port
        resolved.append(True)
        # OSC basic client
        c.connect( fullname,port ) # set the address for all following messages



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
        seed = random.Random() # need to seed first 

        while True:
            ready = select.select([browse_sdRef], [], [])
            if browse_sdRef in ready[0]:
                pybonjour.DNSServiceProcessResult(browse_sdRef)
            rNum= OSC.OSCMessage()
            rNum.setAddress("/print")
            n = seed.randint(1, 1000) # get a random num every loop
            rNum.append(n)
            c.send(rNum)
            time.sleep(5) # wait here some secs

    except KeyboardInterrupt:
        pass
finally:
    browse_sdRef.close()
