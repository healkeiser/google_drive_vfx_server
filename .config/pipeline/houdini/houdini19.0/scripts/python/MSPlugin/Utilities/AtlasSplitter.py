import hou
from .SingletonBase import Singleton

from six import with_metaclass

class AtlasSplitter(with_metaclass(Singleton)):
    def __init__(self):
        pass

    def splitAtlas(self, assetData, importOptions, importParams, materialPath):
        
        atlasMeshOutputs = []
        geometryContainer = hou.node(importParams["assetPath"]).createNode("geo", "Atlas_Splitter")
        if importOptions["UI"]["ImportOptions"]["Renderer"] == "Redshift":
            geometryContainer.parm("RS_objprop_displace_enable").set(1)
            geometryContainer.parm("RS_objprop_displace_scale").set(0.01)

        elif importOptions["UI"]["ImportOptions"]["Renderer"] == "Arnold":
            geometryContainer.parm("ar_disp_height").set(0.008)
        splitterNode = geometryContainer.createNode("quixel_atlas_splitter::1.0")
        opacityMapPath = [opacityMap["path"] for opacityMap in assetData["components"] if opacityMap["type"] == "opacity"]
        
        splitterNode.parm("filename").set(opacityMapPath[0])
        materialNode = splitterNode.createOutputNode("material")
        materialNode.parm("shop_materialpath1").set(materialPath)
        outputNull = materialNode.createOutputNode("null", importParams["assetName"])

        atlasGeometry = outputNull.geometry()
        primitveAttribs = atlasGeometry.primAttribs()
        nameAttrib = [attrib for attrib in primitveAttribs if attrib.name()=="name"][0]
        scatterGroups = nameAttrib.strings()
        for scatterGroup in scatterGroups:
            blastGroup = outputNull.createOutputNode("blast")
            blastGroup.parm("group").set("@name=" + scatterGroup)
            blastGroup.parm("negate").set(1)
            atlasPiece = blastGroup.createOutputNode("null", scatterGroup)
            atlasPiece.setDisplayFlag(True)
            atlasPiece.setRenderFlag(True)
            atlasMeshOutputs.append(atlasPiece)
        geometryContainer.moveToGoodPosition()
        hou.node(importParams["assetPath"]).moveToGoodPosition()
        return atlasMeshOutputs

