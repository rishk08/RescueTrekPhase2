from system import System
# from GUI import GUI  
from GUITesting import GUI  
from InputFeedClasses.IPCamera import IPCamera
# G = GUI(System('config.json'))
# obj = System('config.json')

# obj.StartUp()

# #Determine way to halt main thread and listen for event to shutdown system
# while(True):
#     #Running system
#     i = 0
#     if(i == 1):
#         break;
    
# obj.Shutdown()
camera = IPCamera("0","admin","admin")
camera2 = IPCamera("1","admin","admin")

# G = GUI([camera,camera,camera2,camera2])
# G = GUI([camera, camera2])
G = GUI([camera, camera, camera2])
G.run()


#intiialize GUI with no input parameters
