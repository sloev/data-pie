'''
Created on Oct 27, 2013

@author: sloevWarez
'''

from pylibpd import *
import os


class PatchBay():
    def __init__(self):
        self.fileDirectory='.'
        manager = PdManager(1, 2, 44100, 1)
        self.initPatchList()
    
    def openPatch(self,patchNumber):
        if (patchNumber > 0 and patchNumber < len(self.patchList)):
            self.patch = libpd_open_patch(self.patchList[patchNumber], self.fileDirectory)
            print "$0: ", patch
        else:
            print ("error: patchnumber is not in list")
        
    def closePatch(self):
        libpd_close_patch(self.patch)
    
    def initPatchList(self):
        self.patchList = []
        for files in os.listdir(self.fileDirectory):
            if files.endswith(".pd"):
                self.patchList=[self.patchList , files]
                print("added "+files+" to list")
        
def main():
    pass

if __name__ == '__main__':
    main()