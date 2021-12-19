<div id="top"></div>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/healkeiser/Cioxo">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Google_Drive_logo.png/669px-Google_Drive_logo.png" alt="Logo" width="80" >
  </a>

  <h3 align="center">Google Drive VFX Server</h3>

  <p align="center">
    VFX Pipeline
    <br />
    <br />
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
## Table of Contents
<!--ts-->
   * [About](#about)
   * [Setup Server](#setup)
   * [Software](#software)
      * [Automatic](#automatic)
      * [Manual](#manual)
   * [Tips](#tips)
   * [Roadmap](#roadmap)
   * [Useful Resources and Tools](#useful-resources-and-tools)
   * [Contact](#contact)
<!--te-->

<!-- ABOUT -->
## About
Quick tutorial to setup a Google Drive Server for multiple machines access, and VFX Pipeline on Windows

<!-- SETUP SERVER -->
## Setup Server
- Install [Google Drive File Stream](https://dl.google.com/drive-file-stream/GoogleDriveSetup.exe) and assign the virtual disk the letter `Z:`
> It's important to assign a **similar letter** on every machine at every Google Drive File Stream fresh install, otherwise directories will be broken

- Tick `Stream Files` *(Default Option)*
- Copy the `.config` folder to `Z:/My Drive/` and make it **Available offline** by Right Cliking, `Offline access` > `Available offline` to ensure an access to the files even if the machine is not connected to internet

<!-- SOFTWARE -->
## Software

### Automatic

- Run `Z:/My Drive/.config/environment/environment_source_windows.bat` to setup all the environment variables, or follow instructions under. You can edit the content of the `environment_source_windows.bat` file to adapt it to your needs. Note that you'll still have to configure Substance to use a shared materials library, and run an independant script for After Effects (Detailed in [Manual](#manual) section)
> For example, if you decided to use the letter `F:` (**Not recommended**) for your Google Drive virtual disk, you'll need to edit the first line from `setx PIPELINE_ROOT "Z:/My Drive"` to `setx PIPELINE_ROOT "F:/My Drive"` before executing the file

### Manual

### <img src="https://seeklogo.com/images/P/python-logo-A32636CAA3-seeklogo.com.png" alt="Python" width="15"/> Python

- In construction

### <img src="https://cdn.worldvectorlogo.com/logos/maya-2017.svg" alt="Maya" width="15"/> Maya

- Define a new environment variable for User called *MAYA_APP_DIR*. Give this new variable the value of the folder containing the usual *scripts*, *prefs* folders and so on. This variable needs to be assigned before Maya is started, so writing it in the Maya.env won't work
> Variable should be `MAYA_APP_DIR` `Z:/My Drive/.config/pipeline/maya`

### <img src="https://cdn.worldvectorlogo.com/logos/substance-painter.svg" alt="Substance" width="15"/> Substance Painter
- Define a new environment variable for User called *SUBSTANCE_PAINTER_PLUGINS_PATH*. Give this new variable the value of the folder containing the *python* folder. This variable needs to be assigned before Substance Painter is started
> Variable should be `SUBSTANCE_PAINTER_PLUGINS_PATH` `Z:/My Drive/.config/pipeline/substance_painter/python`

- Open Substance Painter, then open `Modify` > `Settings`. In the new window, go to the `Library` section. In name, type `pipeline_assets` and add the following path: `Z:/My Drive/.config/pipeline/substance_painter/assets`. Click the `+` and restart Substance Painter. Return in `Modify` > `Settings` > `Library` and select the freshly created Library as the default one

[![google-Drive-VFXServer-substance-01.jpg](https://i.postimg.cc/SRW36Xjt/google-Drive-VFXServer-substance-01.jpg)](https://postimg.cc/5Q2s12Bw)

### <img src="https://secure.meetupstatic.com/photos/event/f/a/4/600_466504004.jpeg" alt="Houdini" width="15"/> Houdini

- Define a new environment variable for User called *HSITE*. Give this new variable the value of the parent folder containing the *houdini.major.minor* folder, which contains itself the usual *otls*, *packages* folders and so on. This variable needs to be assigned before Houdini is started, so writing it in the houdini.env won't work
> Variable should be `HSITE` `Z:/My Drive/.config/pipeline/houdini`

- Packages contains a `drive_server.json` file that's specifically dedicated to optimizing the space used on the Google Drive Server if your `PROJECT` folder is there: 10 maximum backup files for each file, and buffered save is activated *at the expense of memory when saving*
> Packages used by Houdini should be there `Z:/My Drive/.config/pipeline/houdini/houdini$HOUDINI_VERSION/packages`

### <img src="https://www.foundry.com/sites/default/files/2021-03/ICON_NUKE-rgb-yellow-01.png" alt="Nuke" width="15"/> Nuke

- Define a new environment variable for User called *NUKE_PATH*. Give this new variable the value of the folder containing the usual *gizmos*, *python* folders and so on. This variable needs to be assigned before Nuke is started
> Variable should be `NUKE_PATH` `Z:/My Drive/.config/pipeline/nuke`

### <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Adobe_After_Effects_CC_icon.svg/512px-Adobe_After_Effects_CC_icon.svg.png" alt="After Effects" width="15"/> After Effects

- You'll need to either manually move the files for After Effects, maybe create a symbolic link (You can use [Link Sell Extension](https://schinagl.priv.at/nt/hardlinkshellext/linkshellextension.html) to do so) between the `$PIPELINE_ROOT/.config/pipeline/after_effects/Support Files` content and your  `C:/Program Files/Adobe/Adobe After Effects $AFTER_EFFECTS_VERSION/Support Files` folder, or use this Python [script](https://github.com/healkeiser/googleDriveVFXServer-pipeline/blob/main/.config/pipeline/after_effects/move_plugins.py) to do it automatically
> Using the Python script, the `Plug-ins` and `Scripts` will only copy in the most recent Adobe After Effects installation folder


<!-- TIPS -->
## Tips
- With that method, you can either place your `PROJECTS` folder on the Google Drive Server freshly created, or leave it anywhere locally
- Here is an example of my `$PIPELINE_ROOT`:

[![google-Drive-VFXServer-01.jpg](https://i.postimg.cc/NMQPzhFY/google-Drive-VFXServer-01.jpg)](https://postimg.cc/sB0cMN50)
- Google Drive will allow you to limit the bandwidth for upload/download directly in the app, which could be useful if the `PROJECTS` folder is saved on the server

<!-- ROADMAP -->
## Roadmap
- [ ] Houdini Packages for levels `Studio`, `Project`, `User`
- [x] Automatic copy of After Effects plug-ins

<!-- RESSOURCES -->
## Useful Resources and Tools
- [MOPS](https://github.com/toadstorm/MOPS "MOPS") - Used in the `.config`
- [JZTREE](https://github.com/joshuazt/JZTREES "JZTREES") - Used in the `.config`
- [AeLib](https://github.com/Aeoll/Aelib "MOPS") - Used in the `.config`
- [qLib](https://github.com/qLab/qLib "qLibS") - Used in the `.config`
- [egMatLib](https://github.com/eglaubauf/egMatLib "egMatLib") - Used in the `.config`
- [Houdini Expression Editor](http://cgtoolbox.com/houdini-expression-editor/ "Houdini Expression Editor") - Used in the `.config`
- [Nuke Survivor Toolkit](https://compositingmentor.com/2020/09/25/nuke-survival-toolkit/ "MOPS") - Used in the `.config`
- [Megascans](https://quixel.com/megascans "Megascans") - Used in the `.config`
- [HSITE](https://www.sidefx.com/docs/houdini/basics/config.html "SideFX: $HSITE")
- [Packages](https://www.sidefx.com/docs/houdini/ref/plugins.html "SideFX: Packages")

<!-- CONTACT -->
## Contact

Valentin Beaumont - [LinkedIn](https://uk.linkedin.com/in/valentin-beaumont) - [Behance](https://www.behance.net/el1ven) - valentin.onze@gmail.com

Project Link: [GoogleDriveServer](https://github.com/healkeiser/googleDriveServer-pipeline)
