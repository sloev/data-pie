'''
Created on Nov 7, 2013

@author: johannes
'''
from Bonjour import Bonjour
from Osc import Osc
import time
import OSC

def main():
    name="oscTestServer"
    regtype='_osc._udp'
    b=Bonjour(name,regtype)
    
    b.runBrowser()
    try:
        c=None
        while(c==None):
            c=b.getFirstClient()            
            time.sleep(1)
        
        osc=Osc(c.name,c.regType)

        while 1:
            string="print LOL"
            msg = OSC.OSCMessage("/print")
            msg.append(string)
            osc.send(msg)            
            time.sleep(4)
    except KeyboardInterrupt:
        b.stopBrowser()
        osc.stopOscServerClient()
    
if __name__ == '__main__':
    main()