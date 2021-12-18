import os
from distutils.dir_util import copy_tree

user = os.getenv('USERNAME')
pipelineRoot = os.getenv('PIPELINE_ROOT')
path_plugins = pipelineRoot + '/.config/pipeline/after_effects/Support Files/Plug-ins'
paths_scripts = pipelineRoot + '/.config/pipeline/after_effects/Support Files/Scripts'
path_adobe = 'C:/Program Files/Adobe/'

if os.path.isdir(path_adobe):
    # ------ Check installations of After Effects and copy files to the most recent one
    list_adobe = os.listdir(path_adobe)
    list_afterEffects = []
    for software in list_adobe:
        if software.startswith('Adobe After Effects'):
            list_afterEffects.append(software)
            list_afterEffects = sorted(list_afterEffects)
    recent_afterEffects = list_afterEffects[-1]
    # ------ TODO: Give user admin privileges to copy in After Effects installation folder
    # ------ Copy folders from .config to After Effects installation
    copy_tree(path_plugins, os.path.join(path_adobe, recent_afterEffects, 'Plug-ins'))
    copy_tree(paths_scripts, os.path.join(path_adobe, recent_afterEffects, 'Scripts'))
    print('Success')
else:
    print('No After Effects installation detected')


