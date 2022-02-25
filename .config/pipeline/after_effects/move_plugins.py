import ctypes
import os
import sys
from distutils.dir_util import copy_tree

pipeline_root = os.getenv("PIPELINE_ROOT")
path_plugins = f"{pipeline_root}/.config/pipeline/after_effects/Support Files/Plug-ins"
paths_scripts = f"{pipeline_root}/.config/pipeline/after_effects/Support Files/Scripts"
path_adobe = "C:/Program Files/Adobe/"


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    if os.path.isdir(path_adobe):
        # ------ Check installations of After Effects and copy files to the most recent one
        list_adobe = os.listdir(path_adobe)
        list_afterEffects = []

        for software in list_adobe:
            if software.startswith("Adobe After Effects"):
                list_afterEffects.append(software)
                list_afterEffects = sorted(list_afterEffects)

        recent_afterEffects = list_afterEffects[-1]
        print(f"Copying to {recent_afterEffects} installation folder...")

        # ------ Copy folders from .config to After Effects installation
        path_plugins_afterEffects = os.path.join(
            path_adobe, recent_afterEffects, "Support Files", "Plug-ins"
        ).replace("\\", "/")
        path_scripts_afterEffects = os.path.join(
            path_adobe, recent_afterEffects, "Support Files", "Scripts"
        ).replace("\\", "/")
        copy_tree(path_plugins.replace("\\", "/"), path_plugins_afterEffects)
        copy_tree(paths_scripts.replace("\\", "/"), path_scripts_afterEffects)

        # ------ Open the Plug-ins and Scripts folders to check files freshly copied
        os.startfile(path_plugins_afterEffects)
        os.startfile(path_scripts_afterEffects)
        print("Success")
        input("\nPress key to exit")
    else:
        print("No After Effects installation detected")
        input("\nPress key to exit")
else:
    # ------ Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
