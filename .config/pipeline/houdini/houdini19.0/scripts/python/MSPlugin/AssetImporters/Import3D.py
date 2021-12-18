
# Workflow machine

from ..Utilities.SettingsManager import SettingsManager
from ..Utilities.SingletonBase import Singleton
from .ImportSurface import ImportSurface
from ..Utilities.MegascansScatter import MegascansScatter
from ..Utilities.USDVariant import *

import hou
import os
import _alembic_hom_extensions as abc
from six import with_metaclass



class ImportUSD(with_metaclass(Singleton)):

    def __init__(self):
        pass

    def importNormalUSD(self, assetData, importOptions, importParams):
        fileextension = os.path.splitext(assetData["meshList"][0]["path"])[1]
        importedAssets = None
        if fileextension !=".abc":  
            importedAssets = self.createObjSetup(assetData, importOptions, importParams)  
        self.usdAssetSetup(importedAssets, assetData, importOptions, importParams)       
        # now setups the imported assets on the USD stage


    def importScatterUSD(self, assetData, importOptions, importParams):
        fileextension = os.path.splitext(assetData["meshList"][0]["path"])[1]
        variantPaths = []
        primitiveBasePath = importOptions['UI']["USDOptions"]["RefPath3D"].rstrip("/") + "/" + importParams["assetName"]
        

        if fileextension ==".abc":
            variantPaths,baseNode = self.scatterAlembicSetup(assetData, importOptions, importParams)

        else:
            variantPaths,baseNode = self.scatterSopSetup(assetData, importOptions, importParams)
            

        primitiveConfigNode = baseNode.createOutputNode("configureprimitive")
        primitiveConfigNode.parm("primpattern").set(primitiveBasePath+"/*")
        primitiveConfigNode.parm("setkind").set(1)
        primitiveConfigNode.parm("kind").set("subcomponent")

        usdMaterialContainer = hou.node(importParams["materialPath"]).createNode("materiallibrary", importParams["assetName"])
        importParams["materialPath"] = usdMaterialContainer.path()
        
        assetMaterial = ImportSurface().importAsset(assetData, importOptions, importParams)
        # usdMaterialContainer.parm("fillmaterials").pressButton()
        usdMaterialContainer.parm("matnode1").set(assetMaterial.name())
        usdMaterialContainer.parm("matpath1").set(usdMaterialContainer.parm("containerpath").eval() + assetMaterial.name())

        matConfigNode = usdMaterialContainer.createOutputNode("configurelayer")

        materialReference = primitiveConfigNode.createOutputNode("reference")
        materialPrimPath =   primitiveBasePath + "/Material"
        materialReference.parm("primpath").set(materialPrimPath)
        materialReference.parm("reftype").set("inputref")

        assignMaterial = materialReference.createOutputNode("assignmaterial")
        # assignMaterial.parm("primpattern1").set(primitiveBasePath + "/*")
        assignMaterial.parm("primpattern1").set(primitiveBasePath + "/*")
        assignMaterial.parm("matspecpath1").set(materialPrimPath + "/" + assetMaterial.name())
        materialReference.setInput(1, matConfigNode)

        variantNode = assignMaterial.createOutputNode("addvariant")
        variantNode.parm("primpath").set(primitiveBasePath)
        variantNode.parm("variantprimpath").set(primitiveBasePath)
        variantNode.parm("createoptionsblock").set(1)

        # hou.node(importParams["usdAssetPath"])
        contextBlock = assignMaterial.createOutputNode("begincontextoptionsblock")
        contextBlock.parm("layerbreak").set(1)

        for variant in variantPaths:
            pruneList = list(variantPaths)
            pruneList.remove(variant)
            pruneNode = contextBlock.createOutputNode("prune")
            pruneNode.parm("num_rules").set(len(variantPaths)-1)
            for i in range(0,len(pruneList)):                
                patternParm = "primpattern" + str(i+1)                
                pruneNode.parm(patternParm).set(pruneList[i])

            variantOut = pruneNode.createOutputNode("null", importParams["assetName"])
            variantNode.insertInput(1, variantOut)

        variantSet = variantNode.createOutputNode("setvariant")
        variantSet.parm("variantset1").set("model")
        variantSet.parm("variantnameuseindex1").set(1)
        # variantSet.parm("variantname1").set(variantPaths[0].split("/")[-1])

        if importOptions["UI"]["USDOptions"]["USDMaterial"] == "Arnold" :
            renderSettings = variantSet.createOutputNode("rendergeometrysettings")
            renderSettings.parm("arnolddisp_height_control").set("set")
            renderSettings.parm("xn__primvarsarnolddisp_height_uhbg").set(0.008)
            variantSet = renderSettings

        outputNode = variantSet.createOutputNode("null", importParams["assetName"])
        outputNode.setDisplayFlag(True)
        #hou.node(importParams["usdAssetPath"]).layoutChildren()
        hou.node(importParams["usdAssetPath"]).moveToGoodPosition()
        
    def scatterAlembicSetup(self, assetData, importOptions, importParams):
        variantPaths = []

        sourceMesh = assetData["meshList"][0]["path"]        
        allObjectsList = abc.alembicGetObjectPathListForMenu(sourceMesh)        
        allObjectsList = list(dict.fromkeys(allObjectsList))        
        pathList = [alembicObject for alembicObject in allObjectsList if alembicObject.endswith(assetData["activeLOD"].upper())]
        
        
        primitiveName = importParams["assetName"]        
        primitiveBasePath = importOptions['UI']["USDOptions"]["RefPath3D"].rstrip("/") + "/" + primitiveName 
        # primitivePath = primitiveBasePath + pathList[0]
        # variantPaths.append(primitivePath)
        # baseNode = hou.node(importParams["usdAssetPath"]).createNode("reference")

        # baseNode.parm("filepath1").set( assetData["meshList"][0]["path"].replace("\\", "/"))
        # baseNode.parm("primpath").set(primitivePath)
        # baseNode.parm("filerefprim1").set("")
        # baseNode.parm("filerefprimpath1").set(pathList[0])
        baseNode = None
        for abcPath in pathList:
            if baseNode == None:
                baseNode = hou.node(importParams["usdAssetPath"]).createNode("reference", abcPath[1:])
            else :
                baseNode = baseNode.createOutputNode("reference", abcPath[1:])

            primitivePath = primitiveBasePath + abcPath + "/Geo"
            variantPaths.append(primitivePath)
            baseNode.parm("filepath1").set( assetData["meshList"][0]["path"].replace("\\", "/"))
            baseNode.parm("primpath").set(primitivePath)
            baseNode.parm("filerefprim1").set("")
            baseNode.parm("filerefprimpath1").set(abcPath)

        transformNode = baseNode.createOutputNode("xform")
        transformNode.parm("scale").set(.01)
        transformNode.parm("primpattern").set(primitiveBasePath)
        

        return variantPaths,transformNode




    def scatterSopSetup(self, assetData, importOptions, importParams):
        variantPaths = []
        scatterSource = self.usdScatterSource(assetData, importOptions, importParams)
        primitiveName = importParams["assetName"] 
        primitiveBasePath = importOptions['UI']["USDOptions"]["RefPath3D"].rstrip("/") + "/" + primitiveName
        primitivePath = primitiveBasePath + "/" + scatterSource[0].name() #+ "/Geo"
        variantPaths.append(primitivePath)

        baseNode = hou.node(importParams["usdAssetPath"]).createNode("sopimport",scatterSource[0].name())
        baseNode.parm("soppath").set(scatterSource[0].path())

        baseNode.parm("primpath").set(primitivePath)
        baseNode.parm("asreference").set(1)
        baseNode.parm("parentprimkind").set("component")

        for scatter in scatterSource[1:]:
            baseNode = baseNode.createOutputNode("sopimport", scatter.name())
            baseNode.parm("soppath").set(scatter.path())                
            baseNode.parm("asreference").set(1)
            baseNode.parm("parentprimkind").set("component")

            primitivePath = primitiveBasePath + "/" + scatter.name() #+ "/Geo"
            baseNode.parm("primpath").set(primitivePath)
            variantPaths.append(primitivePath)

        return variantPaths,baseNode

    def usdAssetSetup(self,  importedAssets,assetData,importOptions, importParams):
        fileextension = os.path.splitext(assetData["meshList"][0]["path"])[1]

        primitvePaths = []
        primitiveName = importParams["assetName"] #+ "_" + importedAssets[0].name()
        primitiveBasePath = importOptions['UI']["USDOptions"]["RefPath3D"].rstrip("/") + "/" + primitiveName
        primitivePath = primitiveBasePath + "/Geo"
        
        primitvePaths.append(primitivePath)

        if fileextension == ".abc":
            baseNode = hou.node(importParams["usdAssetPath"]).createNode("reference",importParams["assetName"])
            baseNode.parm("filepath1").set( assetData["meshList"][0]["path"].replace("\\", "/"))
            baseNode.parm("primpath").set(primitivePath)
            transformNode = baseNode.createOutputNode("xform")
            transformNode.parm("scale").set(.01)
            baseNode = transformNode          


        else:
            baseNode = hou.node(importParams["usdAssetPath"]).createNode("sopimport",assetData["activeLOD"])
            baseNode.parm("soppath").set(importedAssets[0].path())
            baseNode.parm("parentprimkind").set("component")
            baseNode.parm("asreference").set(1)
            baseNode.parm("primpath").set(primitivePath)
        
        # baseNode.parm("parentprimkind").set("Component")
        


        usdMaterialContainer = hou.node(importParams["materialPath"]).createNode("materiallibrary", importParams["assetName"])
        importParams["materialPath"] = usdMaterialContainer.path()        
        
        assetMaterial = ImportSurface().importAsset(assetData, importOptions, importParams)
        # usdMaterialContainer.parm("fillmaterials").pressButton()
        usdMaterialContainer.parm("matnode1").set(assetMaterial.name())
        usdMaterialContainer.parm("matpath1").set(usdMaterialContainer.parm("containerpath").eval() + assetMaterial.name())

        primitiveConfigNode = baseNode.createOutputNode("configureprimitive")
        primitiveConfigNode.parm("primpattern").set(primitivePath)
        primitiveConfigNode.parm("setkind").set(1)
        primitiveConfigNode.parm("kind").set("subcomponent")

        materialReference = primitiveConfigNode.createOutputNode("reference")
        materialPrimPath =   primitiveBasePath + "/Material"
        materialReference.parm("primpath").set(materialPrimPath)
        materialReference.parm("reftype").set("inputref")

        matConfigNode = usdMaterialContainer.createOutputNode("configurelayer")

        assignMaterial = materialReference.createOutputNode("assignmaterial")
        assignMaterial.parm("primpattern1").set(primitivePath)
        assignMaterial.parm("matspecpath1").set(materialPrimPath + "/" + assetMaterial.name())
        materialReference.setInput(1, matConfigNode)

        if importOptions["UI"]["USDOptions"]["USDMaterial"] == "Arnold" :
                renderSettings = assignMaterial.createOutputNode("rendergeometrysettings")
                renderSettings.parm("arnolddisp_height_control").set("set")
                renderSettings.parm("xn__primvarsarnolddisp_height_uhbg").set(0.008)
                assignMaterial = renderSettings


        outputNode = assignMaterial.createOutputNode("null", importParams["assetName"])
        hou.node(importParams["usdAssetPath"]).moveToGoodPosition()
        outputNode.setDisplayFlag(True)

        return outputNode

    def createVariants(self, variantList):
        pass     
            
    def usdScatterSource( self, assetData, importOptions, importParams):
        assetLodsOutput = []
        activeLodGeo = hou.node(importParams["assetPath"]).createNode("geo", assetData["activeLOD"])

        meshSourcePath = assetData["meshList"][0]["path"]
        exportedLod = self.createGeometrySetup(meshSourcePath, activeLodGeo.path(), assetData["activeLOD"])
        assetLodsOutput.append(exportedLod)

        allScatter = {}
        for assetLod in assetLodsOutput:
            if assetData["meshList"][0]["name"].split(".")[-1] == "abc" or assetData["meshList"][0]["name"].split(".")[-1] == "obj":
                allScatter[assetLod.name()] = []
                scatterGroups = [g.name() for g in assetLod.geometry().primGroups()]
                for primGroup in scatterGroups:
                    blastGroup = assetLod.createOutputNode("blast")
                    blastGroup.parm("group").set(primGroup)
                    blastGroup.parm("negate").set(1)
                    varLodOut = blastGroup.createOutputNode("null", primGroup)
                    varLodOut.setRenderFlag(False)
                    
                    # assetLod.setRenderFlag(False)
                    varLodOut.setDisplayFlag(True)
                    varLodOut.setRenderFlag(True)                    
                    allScatter[assetLod.name()].append(varLodOut)


            else:

                allScatter[assetLod.name()] = []
                assetGeometry = assetLod.geometry()
                primitveAttribs = assetGeometry.primAttribs()
                nameAttrib = [attrib for attrib in primitveAttribs if attrib.name()=="name"][0]
                scatterGroups = nameAttrib.strings()            
                for scatterGroup in scatterGroups:
                    blastGroup = assetLod.createOutputNode("blast")
                    blastGroup.parm("group").set("@name=" + scatterGroup)
                    blastGroup.parm("negate").set(1)
                    varLodOut = blastGroup.createOutputNode("null", scatterGroup)
                    varLodOut.setRenderFlag(False)
                    
                    # assetLod.setRenderFlag(False)
                    varLodOut.setDisplayFlag(True)
                    varLodOut.setRenderFlag(True)
                    
                    allScatter[assetLod.name()].append(varLodOut)                   

        
        allVariations = allScatter[assetData["activeLOD"]]
        
        return allVariations

    def createObjSetup(self, assetData, importOptions, importParams):
        assetLodsOutput = []
        geometryContainer = hou.node(importParams["assetPath"]).createNode("geo", importParams["objAssetName"])        
        meshSourcePath = assetData["meshList"][0]["path"]

        exportedLod = self.createGeometrySetup(meshSourcePath, geometryContainer.path(), assetData["activeLOD"])
        assetLodsOutput.append(exportedLod)        

        return assetLodsOutput

    def createGeometrySetup(self, meshSourcePath, targetPath, outputName= "Out"):
        uniformScale = 0.01        
        fileImportNode = hou.node(targetPath).createNode("file")
        fileImportNode.parm("file").set(meshSourcePath)
        transformNode = fileImportNode.createOutputNode("xform")
        transformNode.parm("scale").set(uniformScale)
        outputNullNode = transformNode.createOutputNode("null", outputName)
        return outputNullNode

    def createUsdMaterial(self,assetData, importOptions, importParams):
        usdMaterialContainer = hou.node(importParams["materialPath"]).createNode("materiallibrary", importParams["assetName"])
        importParams["materialPath"] = usdMaterialContainer.path()        
        
        assetMaterial = ImportSurface().importAsset(assetData, importOptions, importParams)
        usdMaterialContainer.parm("fillmaterials").pressButton()

    def getAlembicPaths(self,assetData):
        sourceMesh = assetData["meshList"][0]["path"]
        allObjectsList = abc.alembicGetObjectPathListForMenu(sourceMesh)        
        allObjectsList = list(dict.fromkeys(allObjectsList))
        pathList = [alembicObject for alembicObject in allObjectsList if alembicObject.endswith(assetData["activeLOD"])]








class Import3DAsset(with_metaclass(Singleton)):
    def __init__(self):
        pass

    def importAsset(self, assetData, importOptions, importParams):
        
        self.importType = "usd"
        if self.subType(assetData) == "Scatter":
            if importOptions["UI"]["ImportOptions"]["EnableUSD"]:
                ImportUSD().importScatterUSD(assetData, importOptions, importParams)
            else:

                importedAssets = self.importScatter(assetData, importOptions, importParams)
                assetPaths = [asset.path() for asset in importedAssets ]
                if importOptions["UI"]["ImportOptions"]["UseScattering"]:
                    MegascansScatter().createScatter(assetPaths,None, importParams["assetPath"], importOptions)

                hou.node(importParams["assetPath"]).moveToGoodPosition()

        else :
            if importOptions["UI"]["ImportOptions"]["EnableUSD"]:
                ImportUSD().importNormalUSD(assetData, importOptions, importParams)
                
            else:
                importedAssets = self.importNormal3D(assetData, importOptions, importParams)
                assetPaths = [asset.path() for asset in importedAssets ]
                if importOptions["UI"]["ImportOptions"]["UseScattering"]:
                    MegascansScatter().createScatter(assetPaths,None, importParams["assetPath"], importOptions)
        
                hou.node(importParams["assetPath"]).moveToGoodPosition()
            # /obj/Megascans/3D_Assets/Old_Rusty_Cap_tjxmcjujw



    def subType(self, assetData):
        if "scatter" in assetData["tags"] or "scatter" in assetData["categories"] or  "cmb_asset" in assetData["tags"] or "cmb_asset" in assetData["categories"]: return "Scatter"
        else : return "Normal"

    def importNormal3D(self, assetData, importOptions, importParams):
        assetLodsOutput = []
        geometryContainer = hou.node(importParams["assetPath"]).createNode("geo", "Asset_Geometry")
        materialContainer = hou.node(importParams["assetPath"]).createNode("matnet", "Asset_Material")
        importParams["materialPath"] = materialContainer.path()
        
        assetMaterial = ImportSurface().importAsset(assetData, importOptions, importParams)
        
        assetMaterialPath = ""
        
        if assetMaterial is not None: assetMaterialPath = assetMaterial.path()
        meshSourcePath = assetData["meshList"][0]["path"]
        outputName = importParams["assetName"] + "_" + assetData["activeLOD"]
        exportedLod = self.createGeometrySetup(meshSourcePath,assetMaterialPath, geometryContainer.path(), outputName)
        assetLodsOutput.append(exportedLod)

        if importOptions["UI"]["ImportOptions"]["EnableLods"] :
            selectedOutput = []
            
            for lodData in assetData["lodList"]:                
                
                if assetData["meshList"][0]["name"].split(".")[-1] != lodData["name"].split(".")[-1]:
                    continue

                # need a better condition when lods are 10
                if lodData["lod"] > assetData["activeLOD"] :
                    lodOutputName = importParams["assetName"] + "_" + lodData["lod"]
                    importedLod = self.createGeometrySetup(lodData["path"], assetMaterialPath, geometryContainer.path(), lodOutputName)
                    assetLodsOutput.append(importedLod)

            if len(assetLodsOutput) > 1:
                switchNode = hou.node(geometryContainer.path()).createNode("switch", "LOD_Switch")
                nullOut = switchNode.createOutputNode("null", "SelectedLOD")
                selectedOutput.append(nullOut)
                nullOut.setDisplayFlag(True)
                nullOut.setRenderFlag(True)
                for createdLod in assetLodsOutput:
                    switchNode.setNextInput(createdLod)
                return selectedOutput

        if importOptions["UI"]["ImportOptions"]["Renderer"] == "Redshift":
            geometryContainer.parm("RS_objprop_displace_enable").set(1)            
            geometryContainer.parm("RS_objprop_displace_scale").set(0.01)

        elif importOptions["UI"]["ImportOptions"]["Renderer"] == "Arnold":
            geometryContainer.parm("ar_disp_height").set(0.008)

        geometryContainer.moveToGoodPosition()
        geometryContainer.setSelected(True)
        

        return assetLodsOutput

            
    def createGeometrySetup(self, meshSourcePath, materialPath, targetPath, outputName= "Out"):
        uniformScale = 0.01
        # uniformScale = 1
        fileextension = os.path.splitext(meshSourcePath)[1]
        
        if fileextension == ".abc":
            fileImportNode = hou.node(targetPath).createNode("alembic")
            fileImportNode.parm("fileName").set(meshSourcePath.replace("\\", "/"))
        else :
            fileImportNode = hou.node(targetPath).createNode("file")
            fileImportNode.parm("file").set(meshSourcePath.replace("\\", "/"))
        transformNode = fileImportNode.createOutputNode("xform")
        transformNode.parm("scale").set(uniformScale)
        
        attribDelete = transformNode
        if fileextension == ".fbx":
            attribDelete = transformNode.createOutputNode("attribdelete")
            attribDelete.parm("ptdel").set("fbx_*")

        materialNode = attribDelete.createOutputNode("material")
        materialNode.parm("shop_materialpath1").set(materialPath)
        outputNullNode = materialNode.createOutputNode("null", outputName)
        
        # fileImportNode.setRenderFlag(False)
        outputNullNode.setDisplayFlag(True)
        outputNullNode.setRenderFlag(True)
        
        return outputNullNode

    def importScatter( self, assetData, importOptions, importParams):
        assetLodsOutput = []
        activeLodGeo = hou.node(importParams["assetPath"]).createNode("geo", assetData["activeLOD"])
        activeLodGeo.setSelected(True)
        materialContainer = hou.node(importParams["assetPath"]).createNode("matnet", "Asset_Material")
        importParams["materialPath"] = materialContainer.path()
        assetMaterial = ImportSurface().importAsset(assetData, importOptions, importParams)
        assetMaterialPath = ""
        if assetMaterial is not None: assetMaterialPath = assetMaterial.path()
        
        meshSourcePath = assetData["meshList"][0]["path"]
        exportedLod = self.createGeometrySetup(meshSourcePath,assetMaterialPath, activeLodGeo.path(), assetData["activeLOD"])
        assetLodsOutput.append(exportedLod)

        if importOptions["UI"]["ImportOptions"]["EnableLods"]:
            for lodData in assetData["lodList"]:
                if assetData["meshList"][0]["name"].split(".")[-1] != lodData["name"].split(".")[-1]:
                    continue
                
                # need a better condition when lods are 10
                if lodData["lod"] > assetData["activeLOD"] :
                    lodContainer = hou.node(importParams["assetPath"]).createNode("geo", lodData["lod"])
                    importedLod = self.createGeometrySetup(lodData["path"], assetMaterialPath, lodContainer.path(), lodData["lod"])
                    assetLodsOutput.append(importedLod)
                    if importOptions["UI"]["ImportOptions"]["Renderer"] == "Redshift":
                        lodContainer.parm("RS_objprop_displace_enable").set(1)            
                        lodContainer.parm("RS_objprop_displace_scale").set(0.01)

                    elif importOptions["UI"]["ImportOptions"]["Renderer"] == "Arnold":
                        lodContainer.parm("ar_disp_height").set(0.008)
                   
        allScatter = {}
        for assetLod in assetLodsOutput:
            allScatter[assetLod.name()] = []
            if assetData["meshList"][0]["name"].split(".")[-1] == "abc":
                scatterGroups = list(assetLod.geometry().findPrimAttrib("path").strings())                
                groupPrefix = "@path="
                

            elif assetData["meshList"][0]["name"].split(".")[-1] == "obj":
                allScatter[assetLod.name()] = []
                scatterGroups = [g.name() for g in assetLod.geometry().primGroups()]
                groupPrefix = ""



            else:                
                assetGeometry = assetLod.geometry()
                primitveAttribs = assetGeometry.primAttribs()
                nameAttrib = [attrib for attrib in primitveAttribs if attrib.name()=="name"][0]
                scatterGroups = nameAttrib.strings()
                groupPrefix = "@name="

            for scatterGroup in scatterGroups:
                blastGroup = assetLod.createOutputNode("blast")
                blastGroup.parm("group").set(groupPrefix + scatterGroup)
                blastGroup.parm("negate").set(1)
                varLodOut = blastGroup.createOutputNode("null", scatterGroup.split("/")[-1])                                
                
                varLodOut.setDisplayFlag(True)
                varLodOut.setRenderFlag(True)
                    
                allScatter[assetLod.name()].append(varLodOut)
        
        allVariations = allScatter[assetData["activeLOD"]]

        if importOptions["UI"]["ImportOptions"]["Renderer"] == "Redshift":
            activeLodGeo.parm("RS_objprop_displace_enable").set(1)            
            activeLodGeo.parm("RS_objprop_displace_scale").set(0.01)

        elif importOptions["UI"]["ImportOptions"]["Renderer"] == "Arnold":
            activeLodGeo.parm("ar_disp_height").set(0.008)
        
        return allVariations
        


        # importedAssets = self.importNormal3D(assetData, importOptions, importParams)
        # for importedAsset in importedAssets:
        #     assetGeometry = importedAsset.geometry()
        #     primitveAttribs = assetGeometry.primAttribs()
        #     nameAttrib = [attrib for attrib in primitveAttribs if attrib.name()=="name"][0]
        #     scatterGroups = nameAttrib.strings()
        #     scatterGeometry = hou.node(importParams["assetPath"]).createNode("geo", importedAsset.name())
        #     for scatterGroup in scatterGroups:
                
        #         objMerge = hou.node(scatterGeometry.path()).createNode("object_merge")
        #         objMerge.parm("objpath1").set(importedAsset.path())
        #         objMerge.parm("group1").set("@"+scatterGroup)
        #         objMerge.createOutputNode("null", scatterGroup)


    def scatterSeparator(self, scatterSource):
        pass



    def createAssetTypeRoot(self, assetType):
        pass

    

