
from ..AssetImporters.ImportSurface import ImportSurface
import hou
import os

def alembicReferenceSetup(assetData,importOptions, importParams ):
    variantPaths = []

    primitiveName = importParams["assetName"] 
    primitiveBasePath = importOptions['UI']["USDOptions"]["RefPath3DPlant"].rstrip("/") + "/" + primitiveName

    baseNode = None

    for plantVar in assetData["meshList"]:
        varName = plantVar["name"].split(".")[0]
        primitivePath = primitiveBasePath + "/" + varName + "/" + varName
        if baseNode == None:
             baseNode = hou.node(importParams["usdAssetPath"]).createNode("reference",varName)
        else:
            baseNode = baseNode.createOutputNode("reference", varName)

        baseNode.parm("filepath1").set( plantVar["path"].replace("\\", "/"))
        baseNode.parm("primpath").set(primitivePath)
        variantPaths.append(primitivePath)

    transformNode = baseNode.createOutputNode("xform")
    transformNode.parm("scale").set(.01)
    transformNode.parm("primpattern").set(primitiveBasePath)
    return variantPaths,transformNode



def sopImportSetup(importedAssets,assetData,importOptions, importParams):
    variantPaths = []

    primitiveName = importParams["assetName"] 
    primitiveBasePath = importOptions['UI']["USDOptions"]["RefPath3DPlant"].rstrip("/") + "/" + primitiveName
    primitivePath = primitiveBasePath + "/" + importedAssets[0].name() 
    variantPaths.append(primitivePath)

    baseNode = hou.node(importParams["usdAssetPath"]).createNode("sopimport",importedAssets[0].name())
    baseNode.parm("soppath").set(importedAssets[0].path())

    baseNode.parm("primpath").set(primitivePath)
    baseNode.parm("asreference").set(1)
    baseNode.parm("parentprimkind").set("component")

    for scatter in importedAssets[1:]:
        baseNode = baseNode.createOutputNode("sopimport", scatter.name())
        baseNode.parm("soppath").set(scatter.path())                
        baseNode.parm("asreference").set(1)
        baseNode.parm("parentprimkind").set("component")

        primitivePath = primitiveBasePath + "/" + scatter.name()
        baseNode.parm("primpath").set(primitivePath)
        variantPaths.append(primitivePath)

    return variantPaths,baseNode


def usdVariantSetup(importedAssets,assetData,importOptions, importParams):
    fileextension = os.path.splitext(assetData["meshList"][0]["path"])[1]
    variantPaths = []
    primitiveName = importParams["assetName"]
    primitiveBasePath = importOptions['UI']["USDOptions"]["RefPath3DPlant"].rstrip("/") + "/" + primitiveName

    if fileextension == ".abc":
        variantPaths,baseNode = alembicReferenceSetup(assetData, importOptions, importParams)

    else:
        variantPaths,baseNode = sopImportSetup(importedAssets,assetData, importOptions, importParams)

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
    assignMaterial.parm("primpattern1").set(primitiveBasePath + "/*")
    assignMaterial.parm("matspecpath1").set(materialPrimPath + "/" + assetMaterial.name())
    materialReference.setInput(1, matConfigNode)

    variantNode = assignMaterial.createOutputNode("addvariant")
    variantNode.parm("primpath").set(primitiveBasePath)
    variantNode.parm("variantprimpath").set(primitiveBasePath)
    variantNode.parm("createoptionsblock").set(1)

    
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

        variantOut = pruneNode.createOutputNode("null", variant.split("/")[-1])
        variantNode.insertInput(1, variantOut)

    variantSet = variantNode.createOutputNode("setvariant")
    variantSet.parm("variantset1").set("model")
    variantSet.parm("variantnameuseindex1").set(1)

    if importOptions["UI"]["USDOptions"]["USDMaterial"] == "Arnold" :
        renderSettings = variantSet.createOutputNode("rendergeometrysettings")
        renderSettings.parm("arnolddisp_height_control").set("set")
        renderSettings.parm("xn__primvarsarnolddisp_height_uhbg").set(0.008)
        variantSet = renderSettings
    


    outputNode = variantSet.createOutputNode("null", importParams["assetName"])
    outputNode.setDisplayFlag(True)
    hou.node(importParams["usdAssetPath"]).moveToGoodPosition()