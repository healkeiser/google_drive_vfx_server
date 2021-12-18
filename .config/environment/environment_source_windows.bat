::------
::------ Set environment variables
::------ Change value just under if you have decided to use a diffent virtual drive letter (NOT RECOMMENDED)

setx PIPELINE_ROOT "Z:/My Drive"

::--- Softwares
::------------ Maya
setx MAYA_APP_DIR "%PIPELINE_ROOT%/.config/pipeline/maya"


::------------ Substance Painter
setx SUBSTANCE_PAINTER_PLUGINS_PATH "%PIPELINE_ROOT%/.config/pipeline/substance_painter/python"


::------------ Houdini
setx HSITE "%PIPELINE_ROOT%/.config/pipeline/houdini"


::------------ Nuke
setx NUKE_PATH "%PIPELINE_ROOT%/.config/pipeline/nuke"


pause
