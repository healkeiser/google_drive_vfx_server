

from ..Utilities.SingletonBase import Singleton
from ..MaterialsSetup.MaterialsCreator import MaterialsCreator
from ..MaterialsSetup import *
import hou

from six import with_metaclass

class ImportSurface(with_metaclass(Singleton)):

    def __init_(self):
        pass

    def importAsset(self, assetData, importOptions, importParams):
        
        # asset import parameters
        materialsCreator = MaterialsCreator()
        importedSurface = None
        if not importOptions["UI"]["ImportOptions"]["EnableUSD"]:
            if importOptions["UI"]["ImportOptions"]["Renderer"] == "Redshift" :
                redshiftContainer = hou.node(importParams["materialPath"]).createNode("redshift_vopnet", node_name=importParams["assetName"], run_init_scripts=False)
                
                importParams["materialPath"] = redshiftContainer.path()

            elif importOptions["UI"]["ImportOptions"]["Renderer"] == "Arnold":
                arnoldContainer = hou.node(importParams["materialPath"]).createNode("arnold_materialbuilder", node_name=importParams["assetName"], run_init_scripts=False)
                importParams["materialPath"] = arnoldContainer.path()

            elif importOptions["UI"]["ImportOptions"]["Renderer"] == "Octane":
                octaneContainer = hou.node(importParams["materialPath"]).createNode("octane_vopnet", node_name=importParams["assetName"], run_init_scripts=False)
                importParams["materialPath"] = octaneContainer.path()

            elif importOptions["UI"]["ImportOptions"]["Renderer"] == "Renderman":
                rendermanContainer = hou.node(importParams["materialPath"]).createNode("pxrmaterialbuilder", node_name=importParams["assetName"], run_init_scripts=False)
                importParams["materialPath"] = rendermanContainer.path()

            importedSurface = materialsCreator.createMaterial(importOptions["UI"]["ImportOptions"]["Renderer"], importOptions["UI"]["ImportOptions"]["Material"], assetData, importParams, importOptions)
            
            hou.node(importParams["materialPath"]).moveToGoodPosition()
            hou.node("/mat").moveToGoodPosition()
            importedSurface.setSelected(True)
            if importOptions["UI"]["ImportOptions"]["Renderer"] == "Arnold":
                return arnoldContainer

            if importOptions["UI"]["ImportOptions"]["Renderer"] == "Octane":
                return octaneContainer

            if importOptions["UI"]["ImportOptions"]["Renderer"] == "Redshift":
                return redshiftContainer

            if importOptions["UI"]["ImportOptions"]["Renderer"] == "Renderman":
                return rendermanContainer

            return importedSurface
        
        
        else:
            usdMaterials = {"Mantra" : "Principled Shader", "Renderman" : "Pixar Surface", "Arnold" : "Standard Surface"}
            usdRendererType = importOptions["UI"]["USDOptions"]["USDMaterial"]
            if usdRendererType == "Karma":
                usdRendererType = "Mantra"

            if assetData["type"] == "surface" or assetData["type"] == "atlas" or assetData["type"] == "brush":
                usdMaterialContainer = hou.node(importParams["materialPath"]).createNode("materiallibrary", importParams["assetName"])
                importParams["materialPath"] = usdMaterialContainer.path()

            if importOptions["UI"]["USDOptions"]["USDMaterial"] == "Arnold":
                arnoldContainer = hou.node(importParams["materialPath"]).createNode("arnold_materialbuilder", node_name=importParams["assetName"], run_init_scripts=False)
                importParams["materialPath"] = arnoldContainer.path()
            
            
            importedSurface = materialsCreator.createMaterial(usdRendererType, usdMaterials[usdRendererType], assetData, importParams, importOptions)
            if importOptions["UI"]["USDOptions"]["USDMaterial"] == "Arnold" :
                dispValue = "0.008"
                if assetData["type"] == "surface" or assetData["type"] == "atlas":                    
                    for assetMeta in assetData["meta"]:
                        if assetMeta["key"] == "height":
                            dispValue = assetMeta["value"].split(" ")[0]
                
                    renderSettings = usdMaterialContainer.createOutputNode("rendergeometrysettings")
                    renderSettings.parm("arnolddisp_height_control").set("set")                    
                    renderSettings.parm("xn__primvarsarnolddisp_height_uhbg").set(dispValue)
                    
                importedSurface = arnoldContainer

            if assetData["type"] == "surface" or assetData["type"] == "atlas" or assetData["type"] == "brush":
                usdMaterialContainer.parm("matnode1").set(importedSurface.name())
                usdMaterialContainer.parm("matpath1").set(usdMaterialContainer.parm("containerpath").eval() + importedSurface.name())

            hou.node(importParams["materialPath"]).moveToGoodPosition()
            hou.node("/mat").moveToGoodPosition()
            importedSurface.setSelected(True)

            return importedSurface




        
            
        
        
