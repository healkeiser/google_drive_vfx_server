
from ..Utilities.SingletonBase import Singleton
from .MaterialsCreator import MaterialsCreator
from ..Utilities.RATConverter import *
from ..Utilities.AssetData import *
import hou

class MantraPrincipledMaterial:
    def __init_(self):
        pass
    
    def createMaterial(self, assetData, importParams, importOptions):
        self.principledMaterialSettings = {
            "nodeType" : "principledshader::2.0",
            "defaultParams" : {
                "baseNormal_flipX" : 0,
                "basecolorr" : 1,
                "basecolorg" : 1,
                "basecolorb" : 1,
                "rough" : 1,
                "dispTex_scale" : 0.015,
                "basecolor_usePointColor" : 0

            },
            "textureParams" : {
                "albedo" : {
                    "enableParam" : "basecolor_useTexture",
                    "pathParam" : "basecolor_texture"
                },
                "diffuse" : {
                    "enableParam" : "basecolor_useTexture",
                    "pathParam" : "basecolor_texture"
                },
                "cavity" : {
                    "enableParam" : "ior_useTexture",
                    "pathParam" : "ior_texture"
                },
                "normal" : {
                    "enableParam" : "baseBumpAndNormal_enable",
                    "pathParam" : "baseNormal_texture"
                },
                "metalness" : {
                    "enableParam" : "metallic_useTexture",
                    "pathParam" : "metallic_texture"
                },
                "opacity" : {
                    "enableParam" : "opaccolor_useTexture",
                    "pathParam" : "opaccolor_texture"
                },
                "roughness" : {
                    "enableParam" : "rough_useTexture",
                    "pathParam" : "rough_texture"
                },
                "displacement" : {
                    "enableParam" : "dispTex_enable",
                    "pathParam" : "dispTex_texture"
                },
                "specular" : {
                    "enableParam" : "reflect_useTexture",
                    "pathParam" : "reflect_texture"
                }               
                    

            }
        }
        
        if importOptions["UI"]["ImportOptions"]["ConvertToRAT"] :
            ConvertToRAT(assetData["components"])  

        try :
            materialNode = hou.node(importParams["materialPath"]).createNode(self.principledMaterialSettings["nodeType"], importParams["assetName"])
            self.setMaterialParameters(materialNode, assetData, importOptions)
            if importOptions["UI"]["ImportOptions"]["EnableUSD"] :
                materialNode.parm("dispTex_scale").set("0")

                
                
            return materialNode

        except :
            print ("There was an error creating the Mantra material")
        

    
    def setMaterialParameters(self,materialNode, assetData, importOptions):
        for key in self.principledMaterialSettings["defaultParams"]:

            if assetData["type"] == "surface" and key == "dispTex_scale":
                dispValue = "0.15"
                for assetMeta in assetData["meta"]:
                    if assetMeta["key"] == "height":
                        dispValue = assetMeta["value"].split(" ")[0]
                materialNode.parm(key).set(dispValue)

            else:
                materialNode.parm(key).set(self.principledMaterialSettings["defaultParams"][key])         
        

        for textureData in assetData["components"]:
            if textureData["type"] in self.principledMaterialSettings["textureParams"].keys():
                if textureData["type"] == "metalness":
                    materialNode.parm("metallic").set(1)

                if textureData["type"] == "displacement":
                    if not importOptions["UI"]["ImportOptions"]["ConvertToRAT"] :
                        exrPath = getExrDisplacement(textureData["path"])                            
                        textureData["path"] = exrPath

                    
                materialNode.parm(self.principledMaterialSettings["textureParams"][textureData["type"]]["enableParam"]).set(1)
                materialNode.parm(self.principledMaterialSettings["textureParams"][textureData["type"]]["pathParam"]).set(textureData["path"].replace("\\", "/"))   
                




class MantraTriplanarMaterial:
    def __init__(self):
        pass

    def createMaterial(self, assetData, importParams, importOptions):
        self.triplanarMaterialSettings = {
            "nodeType" : "quixel_mantra_triplanar::1.0",
            "textureParams" : {
                "albedo" : {                   
                    "pathParam" : "ms_albedo"
                },
                "ao" : {                   
                    "pathParam" : "ms_ao"
                },
                "cavity" : {                    
                    "pathParam" : "ms_cavity"
                },
                "bump" : {                   
                    "pathParam" : "ms_bump"
                },
                "normal" : {                   
                    "pathParam" : "ms_normal"
                },
                "gloss" : {
                    "pathParam" : "ms_gloss"
                },
                "fuzz" : {                   
                    "pathParam" : "ms_fuzz"
                },
                "diffuse" : {                   
                    "pathParam" : "ms_diff"
                },
                "mask" : {                   
                    "pathParam" : "ms_mask"
                },
                "normalbump" : {                   
                    "pathParam" : "ms_normalb"
                },
                "metalness" : {                    
                    "pathParam" : "ms_metal"
                },
                "opacity" : {                    
                    "pathParam" : "ms_opac"
                },
                "roughness" : {                    
                    "pathParam" : "ms_rough"
                },
                "displacement" : {                    
                    "pathParam" : "ms_disp"
                },
                "translucency" : {                    
                    "pathParam" : "ms_trans"
                },
                "specular" : {                    
                    "pathParam" : "ms_spec"
                }               
                    

            }
        }

        
        if importOptions["UI"]["ImportOptions"]["ConvertToRAT"] :
            ConvertToRAT(assetData["components"])


        materialNode = hou.node(importParams["materialPath"]).createNode(self.triplanarMaterialSettings["nodeType"], importParams["assetName"])
        
        self.setMaterialParameters(materialNode, assetData)
        return materialNode

    def setMaterialParameters(self,materialNode, assetData):
        for textureData in assetData["components"]:            
            if textureData["type"] in self.triplanarMaterialSettings["textureParams"].keys():              
                materialNode.parm(self.triplanarMaterialSettings["textureParams"][textureData["type"]]["pathParam"]).set(textureData["path"].replace("\\", "/"))



class MantraUSDPrincipled:
    def __init__(self):
        pass

    def createMaterial(self):
        print("USD mantra called")


def registerMantraMaterials():
    
    # materialTypes = ["Principled", "Triplanar"]
    principledCreator = MantraPrincipledMaterial()
    triplanarCreator = MantraTriplanarMaterial()
    usdPrincipledFactory = MantraUSDPrincipled()
    materialsCreator = MaterialsCreator()
    materialsCreator.registerMaterial("Mantra", "Principled Shader", principledCreator.createMaterial)
    # materialsCreator.registerMaterial("Mantra", "Principled_USD", principledCreator.createMaterial)
    materialsCreator.registerMaterial("Mantra", "Triplanar", triplanarCreator.createMaterial)

registerMantraMaterials()




