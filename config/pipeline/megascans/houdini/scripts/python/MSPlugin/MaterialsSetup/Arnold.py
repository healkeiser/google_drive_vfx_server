from ..Utilities.SingletonBase import Singleton
from .MaterialsCreator import MaterialsCreator
from ..Utilities.AssetData import *

import hou

from six import with_metaclass

# "ar_disp_height"

class ArnoldStandardSurfaceFactory(with_metaclass(Singleton)):
    def __init_(self):
        pass
    
    def createMaterial(self, assetData, importParams, importOptions):
        gammaEnabled = ["roughness", "normal", "bump", "displacement", "metalness"]
        
        self.arnoldMaterialSettings = {
            "mapConnections" :{
                "albedo" : {
                    "input" : "base_color",
                    "output" : "rgba"
                },
                "diffuse" : {
                    "input" : "base_color",
                    "output" : "rgba"
                },
                "roughness" : {
                    "input" : "specular_roughness",
                    "output" : "rgba"
                },

                "specular" : {
                    "input" : "specular",
                    "output" : "rgba"
                },
                "normal" : {
                    "input" : "normal",
                    "output" : "vector"
                },
                "bump" : {
                    "input" : "normal",
                    "output" : "vector"
                },
                "opacity" : {
                    "input" : "opacity",
                    "output" : "rgba"
                },
                "displacement" :{
                    "input" : "displacement",
                    "output" : "rgba"
                },
                "metalness" : {
                    "input" : "metalness",
                    "output" : "rgba"
                }
            }

        }
        materialPath = importParams["materialPath"]
        # redshiftMatBuilder = hou.node(materialPath).createNode("redshift_vopnet", importParams["assetName"])
        materialContainer = hou.node(materialPath)        
        shaderNode = materialContainer.createNode("arnold::standard_surface")
        shaderNode.parm("specular").set(0)
        shaderNode.parm("specular_roughness").set(1)
        
        materialNode = materialContainer.createNode("arnold_material", importParams["assetName"])
        
        materialNode.setNamedInput("surface", shaderNode, "shader")

        bumpPriority = False

        normalBumpCombo = False
        normalNode = None
        bumpNode = None

        maptypes = [texture["type"] for texture in assetData["components"] ]
        if "bump" in maptypes and "normal" in maptypes:
            normalBumpCombo = True
            
        for textureData in assetData["components"]:        

            textureNode = materialContainer.createNode("arnold::image", textureData["type"])
            textureNode.parm("filename").set(textureData["path"].replace("\\", "/"))
            if textureData["type"] == "displacement":
                exrPath = getExrDisplacement(textureData["path"])                            
                textureNode.parm("filename").set(exrPath.replace("\\", "/"))

            if textureData["type"] not in self.arnoldMaterialSettings["mapConnections"].keys(): continue

            if assetData["type"] == "surface" or assetData["type"] == "atlas":
                uvTransformNode = materialContainer.createNode("arnold::uv_transform")
                uvTransformNode.setNamedInput("passthrough", textureNode, "rgba")
                textureNode = uvTransformNode

            textureParams =  self.arnoldMaterialSettings["mapConnections"][textureData["type"]]

            if textureData["type"] == "normal":
                normalNode = materialContainer.createNode("arnold::normal_map")
                normalNode.setNamedInput("input", textureNode, "rgba")
                normalNode.parm("color_to_signed").set(0)


                if bumpPriority == False:                    
                    shaderNode.setNamedInput(textureParams["input"], normalNode, textureParams["output"])               


            elif textureData["type"] == "bump":
                bumpNode = materialContainer.createNode("arnold::bump2d")
                bumpNode.parm("bump_height").set(0.5)            
                
                shaderNode.setNamedInput(textureParams["input"], bumpNode, textureParams["output"])   
                bumpNode.setNamedInput("bump_map", textureNode, "rgba")
                bumpPriority = True

            elif textureData["type"] == "displacement":
                materialNode.setNamedInput(textureParams["input"], textureNode, textureParams["output"])
                
               

            else:                
                shaderNode.setNamedInput(textureParams["input"], textureNode, textureParams["output"])

        if normalBumpCombo == True:
            shaderNode.setNamedInput("normal", bumpNode, "vector")
            bumpNode.setNamedInput("normal", normalNode, "vector")



        return materialNode




class ArnoldTriplanarSurfaceFactory(with_metaclass(Singleton)):
    def __init_(self):
        pass
    
    def createMaterial(self, assetData, importParams, importOptions):
        gammaEnabled = ["roughness", "normal", "bump", "displacement", "metalness"]
        
        self.arnoldTriplanarSettings = {
            "mapConnections" : {
                "albedo" : "base_color",
                "diffuse" : "base_color",
                "roughness" : "specular_roughness",
                "specular" : "specular",
                "normal" : "normal",
                "bump" : "normal",
                "opacity" : "opacity",
                "displacement" : "displacement",
                "metalness" : "metalness"
                
            }

            

        }
        materialContainer = hou.node(importParams["materialPath"])
        
        shaderNode = materialContainer.createNode("arnold::standard_surface")
        shaderNode.parm("specular").set(0)
        shaderNode.parm("specular_roughness").set(1)
        
        materialNode = materialContainer.createNode("arnold_material", importParams["assetName"])
        
        materialNode.setNamedInput("surface", shaderNode, "shader")
        triplanarNode = materialContainer.createNode("quixel_arnold_triplanar::1.0")
        
        self.setMaterialParameters(triplanarNode, materialNode,shaderNode, assetData, materialContainer)
        return materialNode

    def setMaterialParameters(self,triplanarNode, materialNode, shaderNode, assetData, materialContainer):
        bumpPriority = False
        normalBumpCombo = False
        maptypes = [texture["type"] for texture in assetData["components"] ]
        if "bump" in maptypes and "normal" in maptypes:
            normalBumpCombo = True


        for textureData in assetData["components"]:
            if triplanarNode.parm(textureData["type"]) is not None:
                triplanarNode.parm(textureData["type"]).set(textureData["path"].replace("\\", "/"))
                if textureData["type"] not in self.arnoldTriplanarSettings["mapConnections"].keys(): continue

                if textureData["type"] == "displacement":
                    materialNode.setNamedInput(self.arnoldTriplanarSettings["mapConnections"][textureData["type"]], triplanarNode, textureData["type"])

                elif textureData["type"] == "normal":
                    normalNode = materialContainer.createNode("arnold::normal_map")
                    normalNode.setNamedInput("input", triplanarNode, "normal")
                    normalNode.parm("color_to_signed").set(0)
                    if bumpPriority == False:           
                        shaderNode.setNamedInput("normal", normalNode, "vector")

                elif textureData["type"] == "bump":
                    bumpNode = materialContainer.createNode("arnold::bump2d")
                    bumpNode.parm("bump_height").set(0.5)
                    shaderNode.setNamedInput("normal", bumpNode, "vector")
                    bumpNode.setNamedInput("bump_map", triplanarNode, "normal")
                    bumpPriority = True

                else:
                    shaderNode.setNamedInput(self.arnoldTriplanarSettings["mapConnections"][textureData["type"]], triplanarNode, textureData["type"])

        if normalBumpCombo == True:
            shaderNode.setNamedInput("normal", bumpNode, "vector")
            bumpNode.setNamedInput("normal", normalNode, "vector")
                




def registerMaterials():    
    
    arnoldStandardFactory = ArnoldStandardSurfaceFactory()
    arnoldTriplanarFactory = ArnoldTriplanarSurfaceFactory()
    materialsCreator = MaterialsCreator()
    materialsCreator.registerMaterial("Arnold", "Standard Triplanar", arnoldTriplanarFactory.createMaterial)
    materialsCreator.registerMaterial("Arnold", "Standard Surface", arnoldStandardFactory.createMaterial)
    
    

registerMaterials()
