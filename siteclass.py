from time import sleep
import constant as const

class Site:
    siteID = ""
    
    def __init__(self, siteId, listOfSensors, listOfModelReferences, configData):
        self.siteID = siteId
    
    def Run(self):
        if("Camera" == const.CAMERA):
            print("Constants work")
        while(True):
            print("Running ", self.siteID)
            sleep(1)
