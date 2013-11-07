'''
Created on Nov 7, 2013

@author: johannes
'''

""" receiving OSC with pyOSC
https://trac.v2.nl/wiki/pyOSC
example by www.ixi-audio.net based on pyOSC documentation

this is a very basic example, for detailed info on pyOSC functionality check the OSC.py file 
or run pydoc pyOSC.py. you can also get the docs by opening a python shell and doing
>>> import OSC
>>> help(OSC)
"""


import OSC
import time, threading,random
class Osc:
    def __init__(self,name="OscTest",regType='_osc._udp',receiveAddress='0.0.0.0',port=None):
        self.name=name
        self.regType=regType
        self.receiveAddress=receiveAddress
        self.port=port
        
        self.initOscClient()
        self.initOscServer()
    
    def getPort(self):
        return self.port
    
    def initOscServer(self):
#         while True:
#             try:
#                 self.port = 9000 + random.randint(0,999)
#                 print "%s: got port %s" % (self.name, self.port)
#                 break
#             except IOError:
#                 print "%s: didn't get port %s" % (self.name, self.port)
        self.oscServer = OSC.OSCServer((self.receiveAddress, self.port),self.oscClient, return_port=self.port)
        self.oscServer.addDefaultHandlers()
        self.oscServer.addMsgHandler("/patchBay", self.patchBayHandler) 
        self.oscServer.addMsgHandler("/print", self.printingHandler) 
        self.oscServer.addMsgHandler("/printed",self.printedReceived)
        
    def initOscClient(self):
        self.oscClient = OSC.OSCClient()
        if(self.port==None):
            while True:
                try:
                    self.port = 9000 + random.randint(0,999)
                    self.oscClient.connect( (self.receiveAddress, self.port) )
                    print "%s: got port %s" % (self.name, self.port)
                    break
                except IOError:
                    print "%s: didn't get port %s" % (self.name, self.port)
        self.oscClient.connect( (self.receiveAddress, self.port) )

    def printedReceived(self,addr, tags, stuff, source):
        
        print "---"
        print "received new osc msg from %s" % OSC.getUrlStr(source)
        print "with addr : %s" % addr
        print "typetags %s" % tags
        print "data %s" % stuff
        print "---"
        
        
    def patchBayHandler(self,addr, tags, stuff, source):

        print "---"
        print "received new osc msg from %s" % OSC.getUrlStr(source)
        print "with addr : %s" % addr
        print "typetags %s" % tags
        print "data %s" % stuff
        print "---"
        
        # send a reply to the client.
        string="%s is printed" % stuff
        msg = OSC.OSCMessage("/printed")
        msg.append(string)
        return msg
        
    def printingHandler(self,addr, tags, stuff, source):
        print "---"
        print "received new osc msg from %s" % OSC.getUrlStr(source)
        print "with addr : %s" % addr
        print "typetags %s" % tags
        print "data %s" % stuff
        print "---"
        

    
    def runOscServerClient(self):
        self.oscServerThread=threading.Thread(target=self.oscServer.serve_forever)
        self.oscServerThread.start()

    
    def stopOscServerClient(self):
        self.oscClient.close()
        try:
            self.oscServer.close()
            self.oscServerThread.join()
        finally:
            pass
    
    def sendTestMessage(self):
        string="print LOL"
        msg = OSC.OSCMessage("/print")
        msg.append(string)
        self.oscClient.send(msg)
    
def main():

    name="oscTestServer"
    regType='_osc._udp'
    
    osc=Osc(name,regType)
    osc.runOscServerClient()
    
    try :
        while 1 :
            time.sleep(5)
            osc.sendTestMessage()
    except KeyboardInterrupt :
        print "\nClosing OSCServer."
        osc.stopOscServerClient()

if __name__ == '__main__':
    main()
        
