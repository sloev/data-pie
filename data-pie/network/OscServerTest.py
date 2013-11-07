'''
Created on Nov 7, 2013

@author: johannes
'''
from Bonjour import Bonjour
from Osc import Osc
import time
def main():
    
    name="oscTestServer"
    regType='_osc._udp'
    
    osc=Osc(name,regType)
    osc.runOscServerClient()
    port=osc.getPort()
    
    a=Bonjour(name,regType,port)
    a.runRegister()
    
    try :
        while 1 :
            time.sleep(5)
    except KeyboardInterrupt :
        print "\nClosing OSCServer."
        osc.stopOscServerClient()
        a.stopRegister()
        
if __name__ == '__main__':
    main()