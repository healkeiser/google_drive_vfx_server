from .SingletonBase import Singleton
from .AssetData import *

import hou

from six import with_metaclass

class MegascansScatter(with_metaclass(Singleton)):
    def __init__(self):
        pass

    def createScatter(self, sourceMeshes, targetMesh, scatterPath, importOptions):
        geometryContainer = hou.node(scatterPath).createNode("geo", "Scatter_Setup")
        if importOptions["UI"]["ImportOptions"]["Renderer"] == "Redshift":
            geometryContainer.parm("RS_objprop_displace_enable").set(1)
            geometryContainer.parm("RS_objprop_displace_scale").set(0.01)

        elif importOptions["UI"]["ImportOptions"]["Renderer"] == "Arnold":
            geometryContainer.parm("ar_disp_height").set(0.008)


        sourceMerge = geometryContainer.createNode("object_merge", "SourceObjects")
        sourceMerge.parm("pack").set(1)
        sourceMerge.parm("numobj").set(len(sourceMeshes))
        for index, sourceMesh in enumerate(sourceMeshes):
            sourceMerge.parm("objpath"+str(index+1)).set(sourceMesh)

        compBegin1 = sourceMerge.createOutputNode("compile_begin")
        blockBegin1 = compBegin1.createOutputNode("block_begin")
        blockBegin1.parm("method").set(3)

        metaBegin1 = hou.node(geometryContainer.path()).createNode("block_begin")
        metaBegin1.parm("method").set(2)

        attWrangle = blockBegin1.createOutputNode("attribwrangle")
        attWrangleVex = "int ittr = detail(1, 'iteration', 0);\n"
        attWrangleVex += "int size = npoints(0);\n"
        attWrangleVex += "if ( @primnum != int( rand( ittr + ch('seed') ) *size ) ) {\n"
        attWrangleVex += "removepoint(0, @ptnum);\n"
        attWrangleVex += "}"
        attWrangle.parm("snippet").set(attWrangleVex)
        attWrangle.setInput(1, metaBegin1)
        if GetMajorVersion() == "18":
            copyPoints = attWrangle.createOutputNode("copytopoints::2.0")

        else :
            copyPoints = attWrangle.createOutputNode("copytopoints")
        blockEnd = copyPoints.createOutputNode("block_end")
        compEnd = blockEnd.createOutputNode("compile_end")

        if targetMesh == None:
            targetMerge = geometryContainer.createNode("grid")
        else:
            targetMerge = hou.node(geometryContainer.path()).createNode("object_merge", "TargetMesh")
            targetMerge.parm("objpath1").set(targetMesh)

        scatterNode = targetMerge.createOutputNode("quixel_simple_scattering::1.0")
        compBegin2 = scatterNode.createOutputNode("compile_begin")
        blockBegin2 = compBegin2.createOutputNode("block_begin")
        blockBegin2.parm("method").set(1)
        copyPoints.setInput(1, blockBegin2)

        compBegin1.parm("blockpath").set(compEnd.path())
        compBegin2.parm("blockpath").set(compEnd.path())
        blockBegin1.parm("blockpath").set(blockEnd.path())
        blockBegin2.parm("blockpath").set(blockEnd.path())
        # metaBegin1.parm("blockpath").set(blockEnd.path())
        blockEnd.parm("blockpath").set(blockBegin2.path())
        blockEnd.parm("templatepath").set(blockBegin2.path())
        blockEnd.parm("itermethod").set(1)
        blockEnd.parm("method").set(1)
        
        # copyPoints.setDisplayFlag(True)
        
        # sourceMerge.setRenderFlag(False)
        # blockBegin2.setRenderFlag(False)
        
        compEnd.setDisplayFlag(True)
        compEnd.setRenderFlag(True)
        
        
        geometryContainer.layoutChildren()

        









        

