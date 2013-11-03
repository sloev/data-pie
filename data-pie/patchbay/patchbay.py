'''
Created on Oct 27, 2013

@author: sloevWarez
'''

from pylibpd import *
import os


class PatchBay():
    def __init__(self):
        self.fileDirectory='.'
        manager = PdManager(0, 1, 44100, 1)
        self.initPatchList()
    
    def openPatch(self,patchNumber):
        try:
            self.patch = libpd_open_patch(self.patchList[patchNumber], self.fileDirectory)
            print "$0: ", self.patch
        except IOError:
            print ("error: patchnumber is not in list")
        
    def closePatch(self):
        libpd_close_patch(self.patch)
    
    def initPatchList(self):
        self.patchList = []
        for files in os.listdir(self.fileDirectory):
            if files.endswith(".pd"):
                self.patchList=[self.patchList , files]
                print("added "+files+" to list")
                
    def getPatchList(self):
        s="/".join(self.patchList)
        return s            
        
def main():
    pass

if __name__ == '__main__':
    main()