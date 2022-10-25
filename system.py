from siteclass import Site
import json
import threading

class System:
    listOfSites = []
    listOfSiteThreads = []
    listOfActiveModels = []
    listOfModelReferences = []
    displayObj = ""
    
    def __init__(self, configFile):
        #Read in config file
        f = open(configFile)
        data = json.load(f)
        
        self.GetListOfActiveModels(data)
        self.InitializeModels()
        self.InitializeSites(data)
        
                    
                    
    def InitializeSites(self, configData):
        sensorData = configData['SensorData']
        for site in configData['ListOfSites']:
            siteId = site['SiteID']
            
            listOfSensors = []
            for sensor in site['ListOfSensors']:
                listOfSensors.append(sensor)

            modelInfo = []
            #Grab a list of all the models that will be used per site
            for sensor in listOfSensors:
                sensorType = sensor['SensorType']
                sensorModels = sensorData[sensorType]['Models']
                modelInfo.append(sensorModels)
            
            listOfModelsForSite = []    
            #Need a loop that reference the listOfModelReferences and create a list of
            #model references that will be utilized for each site
            
            obj = Site(siteId, listOfSensors, listOfModelsForSite, configData)
            self.listOfSites.append(obj)
              
    def InitializeModels(self):
        #Determine how to load in the models and cache them perhaps
        #Save them as a key value pair {SensorType: ModelReference}
        return
                    
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
                
                

