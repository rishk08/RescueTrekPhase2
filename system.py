from siteclass import Site
import json
import threading
from InputFeedClasses.IPCamera import IPCamera
import constant as const
import sys

class System:
    listOfActiveModels = []
    listOfModelReferences = []
    listOfCameras = []
    
    def __init__(self, configFile):
        #Read in config file
        f = open(configFile)
        data = json.load(f)
        
        self.listOfActiveModels = []
        self.listOfModelReferences = []
        
        self.listOfCameras = []
        self.SetCameras(data)
        self.GetListOfActiveModels(data)
        self.InitializeModels()
              
    def InitializeModels(self):
        #Determine how to load in the models and cache them perhaps
        #Save them as a key value pair {SensorType: ModelReference}
        return
    
    def SetCameras(self, configData):
        # siteId = ""
        # location = ""
        # username = ""
        # password = ""
        # ip = ""
        for site in configData['ListOfSites']:
            siteId = ""
            location = ""
            username = ""
            password = ""
            ip = ""
            siteId = site['SiteID']
            location = site['BuildingLocation']
            for sensor in site['ListOfSensors']:
                if(sensor['SensorType'] == const.CAMERA):
                    print(const.CAMERA)
                    ip = sensor['IP']
                    username = sensor['Username']
                    password = sensor['Password']
                    print(ip)
                    print(username)
                    print(password)
                    print(location)
                    camera = IPCamera(ip, username, password, location)
                    print("Camera " + siteId + " is initialized\n")
                    self.listOfCameras.append(camera)
        
        print("initialized cameras")

        
        # i = 1
        # for camera in self.listOfCameras:
        #     # print(camera.location)
        #     if camera == None:
        #         print(i)
        #     i += 1
        # sys.exit(0)
        # for camera in self.listOfCameras:
        #     camera.get_data()
        #     print(i)
        #     i += 1
        # sys.exit()
                    
                
        # camera = IPCamera(ip, username, password, location)
        # print("Camera " + siteId + " is initialized\n")
        # self.listOfCameras.append(camera)
        
    def GetCameras(self):
        return self.listOfCameras
                
                    
    def GetListOfActiveModels(self, configData):
        sensorData = configData['SensorData']
        for site in configData['ListOfSites']:
            siteId = site['SiteID']
            
            listOfSensors = []
            for sensor in site['ListOfSensors']:
                listOfSensors.append(sensor)

            modelInfo = []
            #Grab a list of all the models that will be used
            for sensor in listOfSensors:
                sensorType = sensor['SensorType']
                sensorModels = sensorData[sensorType]['Models']
                modelInfo.append(sensorModels)
            
            #Filter the list of models to unique entires 
            for model in modelInfo:
                if model not in self.listOfActiveModels:
                    self.listOfActiveModels.append(model)
        
    def StartUp(self):
        for i in self.listOfSites:
            thread = threading.Thread(target=i.Run, args=())
            
            thread.start()
            
            self.listOfSiteThreads.append(thread)
            
        #Startup GUI/Display class here, gets it's own thread
        #displayObj = ...
            
    def Shutdown(self):
        #displayObj.Shutdown()
        for i in self.listOfSiteThreads:
            i.join()
                
                

