from ..Utilities.SingletonBase import Singleton
from .MaterialsCreator import MaterialsCreator
from ..Utilities.AssetData import *

import hou

from six import with_metaclass

# RS_Texture: Gamma Override
# RS_Bump: Input Map Type (ie. Tangent Space Normals)

class OctaneUniveralMaterialFactory(with_metaclass(Singleton)):
    def __init_(self):
        pass
    
    def createMaterial(self, assetData, importParams, importOptions):
        gammaCorrected = ["albedo", "diffuse", "specular", "translucency"]
        
        self.octaneMaterialSettings = {
            "mapConnections" :{
                "albedo" : {
                    "input" : "albedo",
                    "output" : "NT_TEX_IMAGE"
                },
                "diffuse" : {
                    "input" : "albedo",
                    "output" : "NT_TEX_IMAGE"
                },
                "roughness" : {
                    "input" : "roughness",
                    "output" : "NT_TEX_IMAGE"
                },

                "specular" : {
                    "input" : "specular",
                    "output" : "NT_TEX_IMAGE"
                },
                "normal" : {
                    "input" : "normal",
                    "output" : "NT_TEX_IMAGE"
                },
                "bump" : {
                    "input" : "bump",
                    "output" : "NT_TEX_IMAGE"
                },
                "opacity" : {
                    "input" : "opacity",
                    "output" : "NT_TEX_IMAGE"
                },
                "displacement" :{
                    "input" : "displacement",
                    "output" : "NT_DISPLACEMENT"
                },
                "metalness" : {
                    "input" : "metallic",
                    "output" : "NT_TEX_IMAGE"
                }
            }

        }
        materialPath = importParams["materialPath"]        
        materialContainer = hou.node(materialPath)        
        shaderNode = materialContainer.createNode("octane::NT_MAT_UNIVERSAL")       
        materialNode = materialContainer.createNode("octane_material")
        materialNode.setNamedInput("material", shaderNode, "NT_MAT_UNIVERSAL")

        if assetData["type"] == "surface" or assetData["type"] == "atlas":
            transformNode = materialContainer.createNode("octane::NT_TRANSFORM_2D")
       
        for textureData in assetData["components"]:            
            
            
            
            
            
            textureNode = materialContainer.createNode("octane::NT_TEX_IMAGE", textureData["type"])
            textureNode.parm("A_FILENAME").set(textureData["path"].replace("\\", "/"))

            

            if textureData["type"] not in gammaCorrected:
                textureNode.parm("gamma").set(1)

            if textureData["type"] not in self.octaneMaterialSettings["mapConnections"].keys(): continue

            textureParams =  self.octaneMaterialSettings["mapConnections"][textureData["type"]]

            if textureData["type"] == "displacement":
                dispNode = materialContainer.createNode("octane::NT_DISPLACEMENT")
                shaderNode.setNamedInput(textureParams["input"], dispNode, textureParams["output"])
                dispNode.setNamedInput("texture", textureNode, "NT_TEX_IMAGE")

                if assetData["type"] == "surface" or assetData["type"] == "atlas":

                    dispValue = "0.15"
                    for assetMeta in assetData["meta"]:
                        if assetMeta["key"] == "height":
                            dispValue = assetMeta["value"].split(" ")[0]                
                    dispNode.parm("amount").set(dispValue)
                else : dispNode.parm("amount").set("0.01")
     

            else:                
                shaderNode.setNamedInput(textureParams["input"], textureNode, textureParams["output"])

            if assetData["type"] == "surface" or assetData["type"] == "atlas":
                textureNode.setNamedInput("transform", transformNode, "NT_TRANSFORM_2D")            



        return materialNode




class OctaneTriplanarUniversalFactory(with_metaclass(Singleton)):
    def __init_(self):
        pass
    
    def createMaterial(self, assetData, importParams, importOptions):
        gammaEnabled = ["roughness", "normal", "bump", "displacement", "metalness"]
        
        self.arnoldTriplanarSettings = {
            "mapConnections" : {
                "albedo" : "albedo",
                "diffuse" : "albedo",
                "roughness" : "roughness",
                "specular" : "specular",
                "normal" : "normal",
                "bump" : "bump",
                "opacity" : "opacity",
                "displacement" : "displacement",
                "metalness" : "metallic"
                
            }            

        }
        materialContainer = hou.node(importParams["materialPath"])
        
        shaderNode = materialContainer.createNode("octane::NT_MAT_UNIVERSAL")
        
        materialNode = materialContainer.createNode("octane_material", importParams["assetName"])
        
        materialNode.setNamedInput("material", shaderNode, "NT_MAT_UNIVERSAL")
        triplanarNode = materialContainer.createNode("quixel_octane_triplanar::1.0")

        dispValue = "0.01"
        if assetData["type"] == "surface" or assetData["type"] == "atlas":            
            for assetMeta in assetData["meta"]:
                if assetMeta["key"] == "height":
                    dispValue = assetMeta["value"].split(" ")[0]          
            

        
        self.setMaterialParameters(triplanarNode, materialNode,shaderNode, assetData, materialContainer, dispValue)
        return materialNode

    def setMaterialParameters(self,triplanarNode, materialNode, shaderNode, assetData, materialContainer, dispValue):
        for textureData in assetData["components"]:            
            if triplanarNode.parm(textureData["type"]) is not None:
                triplanarNode.parm(textureData["type"]).set(textureData["path"].replace("\\", "/"))
                if textureData["type"] not in self.arnoldTriplanarSettings["mapConnections"].keys(): continue

                if textureData["type"] == "displacement":
                    dispNode = materialContainer.createNode("octane::NT_DISPLACEMENT")
                    shaderNode.setNamedInput("displacement", dispNode, "NT_DISPLACEMENT")
                    dispNode.setNamedInput("texture", triplanarNode, "displacement")
                    dispNode.parm("amount").set(dispValue)


                else:
                    shaderNode.setNamedInput(self.arnoldTriplanarSettings["mapConnections"][textureData["type"]], triplanarNode, textureData["type"])
                





def registerMaterials():    
   
    octaneUniversal = OctaneUniveralMaterialFactory()
    octaneTriplanar = OctaneTriplanarUniversalFactory()
    materialsCreator = MaterialsCreator()
    materialsCreator.registerMaterial("Octane", "Universal Material", octaneUniversal.createMaterial)
    materialsCreator.registerMaterial("Octane", "Universal Triplanar", octaneTriplanar.createMaterial)
    

registerMaterials()
