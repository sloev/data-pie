'''
Created on Nov 7, 2013

@author: johannes
'''
from Bonjour import Bonjour
from Osc import Osc

def main():
    name="oscTestServer"
    port=9027
    regtype='_osc._udp'
    
    a=Bonjour(name,regtype,port)
    b=Bonjour(name,regtype,port)
    
    b.runBrowser()
    time.sleep(2)
    a.runRegister()
    index=0
    while index < 10:
        time.sleep(1)
        index=index+1
        print("\n*_*\n")
    a.stopRegister()
    index=0
    while index < 7:
        time.sleep(1)
        index=index+1
        print("\n*_*\n")
    print("stopping browser")
    a.stopRegister()
    print("exiting")
    b.stopBrowser()
    
if __name__ == '__main__':
    main()