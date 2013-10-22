'''
Created on Oct 21, 2013

@author: johannes
'''
from OSC import *
import pybonjour
import threading
import time
import random
import select
'''
heavily based on :
https://github.com/tehn/serialosc/blob/master/profiles/monomeseries.py
'''
class Osc(threading.Thread):
    def __init__(self,serverName):
        print "\n| osc started\t|\n|ctrl-c quits ]\t|\n"
        self.serverName=serverName
        threading.Thread.__init__(self)
        self.exitFlag=0  
        self.osc_server_active = False      
        
    def run(self):

        while not self.osc_server_active:
            try:
                self.port = 9000 + random.randint(0,999)
                self.osc_server = OSCServer(('0.0.0.0', self.port))
                self.osc_server_active = True
            except IOError:
                print "%s: didn't get port %s" % (self.name, self.port)
                            
        self.osc_server.addMsgHandler('default', self.osc_handler)
        self.osc_server_thread = threading.Thread(\
                                                  target=self.osc_server.serve_forever)
        self.osc_server_thread.start()
        print "%s: starting OSC server on port %s" % (self.name, self.port)


        def register_callback(sdRef, flags, errorCode, name, regtype, domain):
            if errorCode == pybonjour.kDNSServiceErr_NoError:
                print 'Registered service:'
                print '  name    =', name
                print '  regtype =', regtype
                print '  domain  =', domain
                
        self.sdRef = pybonjour.DNSServiceRegister(name = "datapie."+self.serverName,
                                     regtype = '_osc._udp',
                                     port = self.port,
                                     callBack = register_callback)
        ready = select.select([self.sdRef], [], [])
        if self.sdRef in ready[0]:
            pybonjour.DNSServiceProcessResult(self.sdRef)
            
        while not self.exitFlag:
            #client stuff / send over osc
            print("still running")
            time.sleep(1)
            
        self.exitRoutine()
        print "Exit success of " + self.serverName

    def stop(self):
        self.exitFlag=1
        print("stop received")
        
    def exitRoutine(self):
        #self.osc_client.close()
        self.osc_server.close()
        self.osc_server_thread.join()
        print "%s: osc server closed" % self.serverName
        self.sdRef.close()
    
    def connectClient(self,dest):
        try:
            self.osc_client.connect(dest)
            print("successfully connected to "+str(dest)+" as a client")
        except OSCClientError:
            #will this actually ever fail??
            print "no destination port?"
                   

    def osc_handler(self, addr, tags, data, client_address):
                """handler for OSCMessages
                - addr (string): The OSC-address pattern of the received Message
                 (the 'addr' string has already been matched against the handler's registerd OSC-address,
                 but may contain '*'s & such)
                - tags (string): The OSC-typetags of the received message's arguments. (without the preceding comma)
                - data (list): The OSCMessage's arguments
                 Note that len(tags) == len(data)
                - client_address ((host, port) tuple): the host & port this message originated from.
                
                a Message-handler function may return None, but it could also return an OSCMessage (or OSCBundle),
                which then gets sent back to the client.
                """
                print "%s: osc: %s %s %s" % (self.name, addr, tags, data)

if __name__ == '__main__':
    thread=Osc("lol")
    thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        thread.stop()
    