import os
import nuke

# ------ Load folders
pipeline_root = os.getenv("PIPELINE_ROOT")
nuke_path = os.getenv("NUKE_PATH")

nuke.pluginAddPath(f"{nuke_path}/plugins/valentin")
nuke.pluginAddPath(f"{nuke_path}/plugins/nuke_survival_toolkit")
