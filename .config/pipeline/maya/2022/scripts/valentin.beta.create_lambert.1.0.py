import maya.cmds as mc
import re

all_meshes = mc.ls(l=True)

for mesh in all_meshes:
    if mc.nodeType(mesh) == 'mesh':
        shape_name = mesh.split('MSH_')[1]
        name = shape_name.replace('Shape','0')
        name = re.sub(r'\W+', '', name) # ------ Stripping illegal characters off
        
        shd = mc.shadingNode('lambert', name='{0}'.format(name), asShader=True)
        shdSG = mc.sets(name='SHD_{0}'.format(name), empty=True, renderable=True, noSurfaceShader=True)
        
        mc.connectAttr('%s.outColor' %shd, '%s.surfaceShader' %shdSG)
        mc.sets(msh, e=True, forceElement=shdSG)
 