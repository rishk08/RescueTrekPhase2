#!/usr/bin/env python3
from time import sleep

class Site:
    siteID = ""
    
    def __init__(self, siteId, listOfSensors, listOfModelReferences, configData):
        self.siteID = siteId
    
    def Run(self):
        while(True):
            print("Running ", self.siteID)
            sleep(1)
