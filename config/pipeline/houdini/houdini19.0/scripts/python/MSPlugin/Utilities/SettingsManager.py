
from .SingletonBase import Singleton
import os
import json

from six import with_metaclass


class SettingsManager(with_metaclass(Singleton)):

    def __init_(self):
        pass        
        
    def getSettings(self):
        self.settings = self.__loadSettings()
        return self.settings

    def __loadSettings(self):
        settingsFilePath = self.getSettingsPath()
        
        if settingsFilePath == None:
            return None
        try:
            with open(settingsFilePath, 'r') as fl_:
                settings =  json.load(fl_)
                if self.checkSettingsValidity(settings):
                    return settings
                else:
                    defaultSettings = self.createDefaultSettings(settingsFilePath)
                    self.saveSettings(defaultSettings)
                    return defaultSettings


        except Exception as e:
            print("Error reading json file")
            defaultSettings = self.createDefaultSettings(settingsFilePath)
            return defaultSettings


    def createDefaultSettings(self, settingsFilePath):
        try:
            defaultSettings = { "UI" : { "ImportOptions" : { "Renderer" : "Mantra", "Material" : "Principled Shader", "UseScattering" : False, "UseExrDisplacement" : False, "UseAtlasSplitter" : False, "EnableLods" : False, "ApplyMotion" : False, "EnableUSD" : False , "ConvertToRAT" : True}, "USDOptions" : { "USDMaterial" : "Karma", "3DrefPath" : "/Megascans/_3D_Assets/", "3DPlantRefPath" : "/Megascans/_3D_Plants/", "SurfaceRefPath" : "/Megascans/Surfaces", "ImportLods" : False } }, "Misc" : { } }
            with open(settingsFilePath, 'w') as outfile:
                json.dump(defaultSettings, outfile)
            return defaultSettings    
                        
        except Exception as e:
            return defaultSettings
        

    def getSettingsPath(self):
        settingsPath = self.getEnvironmentPath()
        if settingsPath == None:
            settingsFilename = "Settings.json"
            settingsPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))           
           
            if os.access(settingsPath, os.W_OK):
                settingsFilePath = os.path.join(settingsPath, settingsFilename)
                if os.path.isfile(settingsFilePath):                    
                    if not os.access(settingsFilePath, os.W_OK):                   
                        return None
                    else:
                        return settingsFilePath

                else :
                    try:
                        settingsFile = open(settingsFilePath, "w+")
                        settingsFile.close()
                        return settingsFilePath
                    except Exception as e:
                        return None
                
            else :
                return None
        else :
            return settingsPath



    def getEnvironmentPath(self):
            

        fileName = "Settings.json"
        savePath = os.getenv("MS_HOUDINI_PATH")
        
        if savePath != None :            
            settingsPath = os.path.join(savePath, fileName)
            if os.path.exists(savePath):
                
                if os.access(savePath, os.W_OK) == False :
                    return None

                if os.path.isfile(settingsPath):
                    if os.access(settingsPath, os.W_OK) == False:
                        return None
                    else :
                        return settingsPath
                try:
                    settingsFile = open(settingsPath, "w+")
                    settingsFile.close()
                    return settingsPath
                except Exception as e:
                    return None                

            else:

                try:                    
                    os.makedirs(savePath)
                    settingsFile = open(settingsPath, "w+")
                    settingsFile.close()
                    return settingsPath
                except Exception as e:
                    return None

        return None


        


    def saveSettings(self, settings):
        try:
            self.settings = settings
            settingsFilePath = self.getSettingsPath()
            if settingsFilePath == None:
                return

            with open(settingsFilePath, 'w') as outfile:
                json.dump(settings, outfile)

            
        except Exception as e:
            pass

    def updateSetting(self, setting_key, setting_value):
        pass

    def updateSettings(self, settings):
        pass

    def checkSettingsValidity(self, settings):
        # needs to be pythonic and complete
        if "UI" in settings.keys():
            if "ImportOptions" in settings["UI"].keys():                           
                return True
        return False
