#import histogram as w
from system import System
    
obj = System('config.json')

obj.StartUp()

#Determine way to halt main thread and listen for event to shutdown system
while(True):
    #Running system
    i = 0
    if(i == 1):
        break;
    
obj.Shutdown()

#w.webcamCV()
