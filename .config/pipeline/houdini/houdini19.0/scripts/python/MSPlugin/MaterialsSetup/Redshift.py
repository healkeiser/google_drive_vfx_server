

from ..Utilities.SingletonBase import Singleton
from .MaterialsCreator import MaterialsCreator
from ..Utilities.AssetData import *

import hou

from six import with_metaclass

class RedshiftMaterialFactory(with_metaclass(Singleton)):
    def __init_(self):
        pass
    
    def createMaterial(self, assetData, importParams, importOptions):
        gammaCorrected = ["albedo", "diffuse", "specular", "translucency"]
        
        self.redshiftMaterialSettings = {
            "mapConnections" :{
                "albedo" : {
                    "input" : "diffuse_color",
                    "output" : "outColor"
                },
                "translucency" : {
                    "input" : "transl_color",
                    "output" : "outColor"
                },
                "diffuse" : {
                    "input" : "diffuse_color",
                    "output" : "outColor"
                },

                "roughness" : {
                    "input" : "refl_roughness",
                    "output" : "outColor"
                },

                "specular" : {
                    "input" : "refl_color",
                    "output" : "outColor"
                },
                "normal" : {
                    "input" : "Bump Map",
                    "output" : "out"
                },
                "bump" : {
                    "input" : "Bump Map",
                    "output" : "out"
                },
                "opacity" : {
                    "input" : "opacity_color",
                    "output" : "outColor"
                },
                "displacement" :{
                    "input" : "Displacement",
                    "output" : "out"
                },
                "metalness" : {
                    "input" : "refl_metalness",
                    "output" : "outR"
                },
                "cavity" : {
                    "input" : "overall_color",
                    "output" : "outColor"
                }
            }

        }
        materialPath = importParams["materialPath"]
        # redshiftMatBuilder = hou.node(materialPath).createNode("redshift_vopnet", importParams["assetName"])
        materialContainer = hou.node(materialPath)        
        shaderNode = materialContainer.createNode("redshift::Material")
        shaderNode.parm("refl_brdf").set("1")
        # shaderNode.parm("refl_fresnel_mode").set("2")
        materialNode = materialContainer.createNode("redshift_material", importParams["assetName"])
        materialNode.setNamedInput("Surface", shaderNode, "outColor")

        normalPriority = False      
 
        for textureData in assetData["components"]:

            if textureData["type"] != "opacity":
                textureNode = materialContainer.createNode("redshift::TextureSampler", textureData["type"])
                textureNode.parm("tex0").set(textureData["path"].replace("\\", "/"))

            if textureData["type"] not in self.redshiftMaterialSettings["mapConnections"].keys(): continue
            textureParams =  self.redshiftMaterialSettings["mapConnections"][textureData["type"]]

            if textureData["type"] == "translucency":
                shaderNode.parm("transl_weight").set(0.5)

            # if textureData["type"] in gammaEnabled:
            #     textureNode.parm("tex0_gammaoverride").set(1)

            if textureData["type"] == "roughness":
                rampNode = materialContainer.createNode("redshift::RSRamp")
                rampNode.setNamedInput("input", textureNode, "outColor" )                
                shaderNode.setNamedInput(textureParams["input"], rampNode, textureParams["output"])

            elif textureData["type"] == "opacity":
                spriteNode = materialContainer.createNode("redshift::Sprite")
                spriteNode.setNamedInput("input", shaderNode, "outColor")
                materialNode.setNamedInput("Surface", spriteNode, "outColor")
                spriteNode.parm("tex0").set(textureData["path"].replace("\\", "/"))

            elif textureData["type"] == "metalness":
                channelSplitter2 = materialContainer.createNode("redshift::RSColorSplitter")
                shaderNode.setNamedInput(textureParams["input"], channelSplitter2, textureParams["output"])
                channelSplitter2.setNamedInput("input", textureNode, "outColor" )

            elif textureData["type"] == "normal":
                normalNode = materialContainer.createNode("redshift::BumpMap")
                normalNode.parm("inputType").set("1")                

                materialNode.setNamedInput(textureParams["input"], normalNode, textureParams["output"])
                normalNode.setNamedInput("input", textureNode, "outColor")
                normalPriority = True                
                

            elif textureData["type"] == "bump":
                bumpNode = materialContainer.createNode("redshift::BumpMap")                
                if normalPriority == False:
                    materialNode.setNamedInput(textureParams["input"], bumpNode, textureParams["output"])   
                bumpNode.setNamedInput("input", textureNode, "outColor")              
            

            elif textureData["type"] == "displacement":
                exrPath = getExrDisplacement(textureData["path"])                
                textureNode.parm("tex0").set(exrPath.replace("\\", "/"))
                dispNode = materialContainer.createNode("redshift::Displacement")


                materialNode.setNamedInput(textureParams["input"], dispNode, textureParams["output"])
                dispNode.setNamedInput("texMap", textureNode, "outColor")

            elif textureData["type"] == "albedo" or textureData["type"] == "diffuse":
                ccNode = materialContainer.createNode("redshift::RSColorCorrection")
                ccNode.setNamedInput("input", textureNode, "outColor")
                shaderNode.setNamedInput("diffuse_color", ccNode, "outColor")

              

            else:                
                shaderNode.setNamedInput(textureParams["input"], textureNode, textureParams["output"])
                


            
           

        return materialNode


class RedshiftTriplanarFactory(with_metaclass(Singleton)):
    def __init__(self):
        pass

    def createMaterial(self, assetData, importParams, importOptions):
        self.triplanarSettings = {
            "mapConnections" : {
                "albedo" : "diffuse_color",
                "diffuse" : "diffuse_color",
                "roughness" : "refl_roughness",
                "specular" : "refl_reflectivity",
                "normal" : "bump_input",
                "bump" : "Bump Map",
                "opacity" : "opacity_color",
                "displacement" : "Displacement",
                "metalness" : "refl_metalness"
                
            }

        }

        materialContainer = hou.node(importParams["materialPath"])        
        shaderNode = materialContainer.createNode("redshift::Material")
        shaderNode.parm("refl_brdf").set("1")
        # shaderNode.parm("refl_fresnel_mode").set("2")
        materialNode = materialContainer.createNode("redshift_material", importParams["assetName"])
        materialNode.setNamedInput("Surface", shaderNode, "outColor")
        triplanarNode = materialContainer.createNode("quixel_redshift_triplanar::1.0")
        for textureData in assetData["components"]:            
            if triplanarNode.parm(textureData["type"]) is not None:
                triplanarNode.parm(textureData["type"]).set(textureData["path"].replace("\\", "/"))
                if textureData["type"] not in self.triplanarSettings["mapConnections"].keys(): continue

                if textureData["type"] == "displacement":
                    dispNode = materialContainer.createNode("redshift::Displacement")
                    materialNode.setNamedInput("Displacement", dispNode, "out")
                    dispNode.setNamedInput("texMap", triplanarNode, "displacement")

                elif textureData["type"] == "bump" :
                    bumpNode = materialContainer.createNode("redshift::BumpMap")
                    materialNode.setNamedInput("Bump Map", bumpNode, "out")   
                    bumpNode.setNamedInput("input", triplanarNode, "bump")
                else:
                    shaderNode.setNamedInput(self.triplanarSettings["mapConnections"][textureData["type"]], triplanarNode, textureData["type"])

        return materialNode

       



def registerMaterials():
    
    # materialTypes = ["Principled", "Triplanar"]
    redshiftTextures = RedshiftMaterialFactory()
    redshiftTriplanar = RedshiftTriplanarFactory()
    materialsCreator = MaterialsCreator()
    materialsCreator.registerMaterial("Redshift", "Redshift Material", redshiftTextures.createMaterial)
    materialsCreator.registerMaterial("Redshift", "Redshift Triplanar", redshiftTriplanar.createMaterial)
    

registerMaterials()
