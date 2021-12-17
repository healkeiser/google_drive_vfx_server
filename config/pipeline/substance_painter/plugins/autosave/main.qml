import QtQuick 2.7
import Painter 1.0

PainterPlugin
{
  ConfigurationStruct {
    id: config
  }

  // timer to display the popup since WorkerScript cannot be used
  // with alg context
  Timer
  {
    id: savePostProcess
    repeat: false
    interval: 1
    onTriggered: {
      try {
        if (!internal.projectOpen) return
        alg.log.info("Auto saving project (backup number " + config.actualFileIndex + ")...");
        var origPath;
        var projectIsSaved = true;
        try {
          alg.project.url();
        }
        catch(e) {
          projectIsSaved = false
        }
        if (!projectIsSaved) {
          // use config default
          if (config.tempFileName === "") {
            var date = new Date()
            config.tempFileName = date.toLocaleString(Qt.locale(), "dd_MM_yyyy_hh_mm")
          }
          origPath = config.saveDirectoryPath + config.tempFileName + ".spp"
        }
        else origPath = alg.fileIO.urlToLocalFile(alg.project.url());
        // remove extension
        var pathTemplate = origPath.replace(/\.[^\.]*$/, "")
        // replace path if needed
        if (config.alwaysUseSaveDirectory) {
          pathTemplate = pathTemplate.replace(/^.*\//, config.saveDirectoryPath)
        }
        pathTemplate = alg.fileIO.localFileToUrl(pathTemplate)

        alg.project.saveAsCopy(pathTemplate + "_autosave_" + config.actualFileIndex + ".spp")

        internal.incrFileIndex()
        // close() is disable for the popup, we must affect visible directly
        savePopup.visible = false
      }
      catch(err) {
        alg.log.exception(err)
        savePopup.visible = false
      }
    }
  }

  QtObject {
    id: internal
    property bool projectOpen: alg.project.isOpen()
    readonly property alias saving: savePopup.visible
    property bool computing: false
    property bool busy: false
    property bool startProgress: false
    onProjectOpenChanged: {
      if (projectOpen) {
        reinitRemainingTime()
        timer.start()
      }
      else timer.stop()
    }

    function incrFileIndex() {
      ++config.actualFileIndex;
      if (config.actualFileIndex >= config.filesNumber) config.actualFileIndex = 0
    }

    function save() {
      if(alg.project.needSaving())
      {
        alg.log.info("Autosaving...");
        savePopup.visible = true
        savePostProcess.start()
      }
    }

    function initRemainingTime(toTime) {
      internal.startProgress = config.warningTime >= toTime
      config.remainingTime = toTime
    }

    function reinitRemainingTime() {
      initRemainingTime(config.interval)
    }

    function snooze() {
      initRemainingTime(config.snooze)
    }

    function onProjectChange() {
      projectOpen = true
      config.actualFileIndex = 0
    }
  }

  Timer
  {
    id: timer
    repeat: true
    interval: 1000
    onTriggered: {
      if (!internal.saving && config.remainingTime != 0) --config.remainingTime;
      // reinitialize timer if null
      if (config.remainingTime <= config.warningTime) {
        internal.startProgress = true;
        // If computing, wait until computation end and painter is not busy
        if (internal.computing || internal.busy) return
        if (config.remainingTime == 0) {
          internal.save();
          internal.reinitRemainingTime()
        }
      }
    }
  }

  Component.onCompleted:
  {
    // save button
    var snoozeButton = alg.ui.addWidgetToPluginToolBar( "SnoozeButton.qml" )
    // bind remaining time and saving values
    snoozeButton.remainingTime = Qt.binding(function() { return config.remainingTime })
    snoozeButton.startProgress = Qt.binding(function() { return internal.startProgress })
    snoozeButton.saving = Qt.binding(function() { return internal.saving })
    snoozeButton.progressMaxValue = Qt.binding(function() { return config.warningTime })
    snoozeButton.active = Qt.binding(function() { return internal.projectOpen })
    // bind button status
    snoozeButton.clicked.connect(internal.snooze)
  }

  onProjectSaved: internal.reinitRemainingTime()

  onProjectAboutToClose: {
    config.tempFileName = ""
    internal.projectOpen = false
  }

  onProjectOpened: internal.onProjectChange()

  onNewProjectCreated: internal.onProjectChange()

  onComputationStatusChanged: {
    internal.computing = isComputing
  }

  onBusyStatusChanged: {
    internal.busy = busy
  }

  onConfigure:
  {
    configDialog.open();
  }

  ConfigurePanel
  {
    id: configDialog

    onVisibleChanged: {
      if (visible) timer.stop()
      else if (internal.projectOpen) timer.restart()
    }

    onConfigurationChanged: {
      config.interval = interval
      config.filesNumber = filesNumber
      if (config.actualFileIndex >= filesNumber) config.actualFileIndex = 0
      config.snooze = snooze
      config.warningTime = warningTime
      config.saveDirectoryPath = saveDirectoryPath
      config.alwaysUseSaveDirectory = alwaysUseSaveDirectory
      if (config.remainingTime == 0 || config.remainingTime > config.interval)
        internal.reinitRemainingTime();
    }
  }

  SavePopup {
    id: savePopup
  }
}
