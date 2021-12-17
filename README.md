<div id="top"></div>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/healkeiser/Cioxo">
    <img src="all/ui/graphics/logos/cioxoLogo_border.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Google Driver Server Pipeline</h3>

  <p align="center">
    Cioxo Pipeline
    <br />
    <br />
    <br />

</div>

<!-- ABOUT THE PROJECT -->
## About The Project
Quick tutorial to setup a Google Drive Server for multiple machines access and VFX Pipeline


<!-- SETUP SERVER -->
## Setup Server
- Install [Google Drive File Stream](https://dl.google.com/drive-file-stream/GoogleDriveSetup.exe) and assign the virtual disk the letter `Z:`
> It's important to assign a **similar letter** on every machine at every Google Drive File Stream fresh install, otherwise directories will be broken

- In `Z:/My Drive/` make the folder `.config` **Available offline** by Right Cliking, `Offline access` > `Available offline` to ensure an access to the files even if the machine is not connected to internet


<!-- SOFTWARE -->
## Software

### Automatic

- Run `Z:/My Drive/.config/environment/environment_source_windows.bat` to setup all the environment variables, or follow instructions under. You can edit the content of the `environment_source_windows.bat` file to adapt it to your needs
> For example, if you decided to use the letter `F:` (**Not recommended**) for your Google Drive virtual disk, you'll need to edit the first line from `setx PIPELINE_ROOT "Z:/My Drive"` to `setx PIPELINE_ROOT "F:/My Drive"` before executing the file


### Manual
### ![#1589F0](https://via.placeholder.com/15/1589F0/000000?text=+) Maya

- Define a new environment variable for User called *MAYA_APP_DIR*. Give this new variable the value of the folder containing the usual *scripts*, *prefs* folders and so on. This variable needs to be assigned before Maya is started, so writing it in the Maya.env won't work
> Variable should be `MAYA_APP_DIR` `Z:/My Drive/.config/pipeline/maya`

- In **Prism > User Settings > DCC Apps > Maya > Prism Integrations**, select Save As `.mb` instead of `.ma`. Files will be lighter, but impossible to open as text

### ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) Substance Painter
- Define a new environment variable for User called *SUBSTANCE_PAINTER_PLUGINS_PATH*. Give this new variable the value of the folder containing the *python* folder. This variable needs to be assigned before Substance Painter is started
> Variable should be `SUBSTANCE_PAINTER_PLUGINS_PATH` `Z:/My Drive/.config/pipeline/substance_painter/python`

### ![#FD7F20](https://via.placeholder.com/15/FD7F20/000000?text=+) Houdini

- Define a new environment variable for User called *HSITE*. Give this new variable the value of the parent folder containing the *houdini.major.minor* folder, which contains itself the usual *otls*, *packages* folders and so on. This variable needs to be assigned before Houdini is started, so writing it in the houdini.env won't work
> Variable should be `HSITE` `Z:/My Drive/.config/pipeline/houdini`

- Packages contains a `04_drive_server` part that's specifically dedicated to optimizing the space used on the Google Drive Server: 10 maximum backup files for each file, and buffered save is activated *at the expense of memory when saving*
> Packages used by Houdini should be there `Z:/My Drive/.config/pipeline/houdini/houdini$HOUDINI_VERSION/packages`

### ![#FFFF00](https://via.placeholder.com/15/FFFF00/000000?text=+) Nuke

- Define a new environment variable for User called *NUKE_PATH*. Give this new variable the value of the folder containing the usual *gizmos*, *python* folders and so on. This variable needs to be assigned before Nuke is started
> Variable should be `NUKE_PATH` `Z:/My Drive/.config/pipeline/nuke`

- In **Prism > User Settings > DCC Apps > Nuke > Prism Integrations**, tick *Use NukeX instead of Nuke*


## To-Do List
- [ ] Packages for levels `Studio`, `Project`, `User`

### Ideas
```
- Using a *SymbolicLink* for some files in between the Google Drive Server and the personal machine
- Script to prevent files too big to upload/download (See Prism compatibility) or simply limit bandwidth in Google Drive File Stream
- Script to Archive projects, or simply move them to a secure offline location while done
```


## Useful Resources
- [HSITE](https://www.sidefx.com/docs/houdini/basics/config.html "SideFX: $HSITE")
- [Packages](https://www.sidefx.com/docs/houdini/ref/plugins.html "SideFX: Packages")



## Markdown
### Colors
![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) `#red`
![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+) `#green`
![#1589F0](https://via.placeholder.com/15/1589F0/000000?text=+) `#blue`
![#FD7F20](https://via.placeholder.com/15/FD7F20/000000?text=+) `#orange`
![#FFFF00](https://via.placeholder.com/15/FFFF00/000000?text=+) `#yellow`
