import QtQuick 2.5
import QtQml 2.2
import QtQml.Models 2.2
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.2
import AlgWidgets 2.0
import AlgWidgets.Style 2.0

AlgDialog
{
  id: root;
  visible: false;
  title: qsTr("Autosave configuration");
  width: 400;
  height: 280;
  minimumWidth: width;
  minimumHeight: height;
  maximumWidth: width;
  maximumHeight: height;

  signal configurationChanged(
    int interval,
    int filesNumber,
    int snooze,
    int warningTime,
    string saveDirectoryPath,
    bool alwaysUseSaveDirectory)

  onVisibleChanged: {
    if (visible) internal.initModel()
  }

  Component.onCompleted: {
    internal.initModel()
    internal.emit()
  }

  onAccepted: internal.emit()

  QtObject {
    id: internal
    readonly property string intervalKey:           "autosaveInterval"
    readonly property string filesNumberKey:        "autosaveNumber"
    readonly property string snoozeKey:             "snooze"
    readonly property string warningTimeKey:        "warningTime"
    readonly property string saveDirectoryKey:      "autosaveDirectory"
    readonly property string useDirectoryKey:       "useAutosaveDirectory"
    readonly property int intervalDefault:          30
    readonly property int filesNumberDefault:       2
    readonly property int snoozeDefault:            5
    readonly property int warningTimeDefault:       20
    readonly property string saveDirectoryDefault:  alg.documents_directory + "autosave/"
    readonly property bool useDirectoryDefault:     false
    readonly property int intervalMax:              120
    readonly property int filesNumberMax:           50
    readonly property int snoozeMax:                15
    readonly property int warningTimeMax:           60

    property var settings: ({})

    function newModelComponent(label, min_value, max_value, default_value, settings_name) {
      return {
        "label": label,
        "min_value": min_value,
        "max_value": max_value,
        "default_value": default_value,
        "settings_name": settings_name
      }
    }

    function initModel() {
      reinitSettings()
      model.clear()
      model.append(
        newModelComponent(
          qsTr("Autosave interval in minutes:"),
          10,
          intervalMax,
          intervalDefault,
          intervalKey))
      model.append(
        newModelComponent(
          qsTr("Number of autosave files:"),
          1,
          filesNumberMax,
          filesNumberDefault,
          filesNumberKey))
      model.append(
        newModelComponent(
          qsTr("Snooze interval in minutes:"),
          1,
          snoozeMax,
          snoozeDefault,
          snoozeKey))
      model.append(
        newModelComponent(
          qsTr("Warning time before save in seconds:"),
          10,
          warningTimeMax,
          warningTimeDefault,
          warningTimeKey))
    }

    function reinitSettings() {
      updateSettings(intervalKey, alg.settings.value(intervalKey, intervalDefault))
      updateSettings(filesNumberKey, alg.settings.value(filesNumberKey, filesNumberDefault))
      updateSettings(snoozeKey, alg.settings.value(snoozeKey, snoozeDefault))
      updateSettings(warningTimeKey, alg.settings.value(warningTimeKey, warningTimeDefault))
      updateSettings(saveDirectoryKey, alg.settings.value(saveDirectoryKey, saveDirectoryDefault))
      updateSettings(useDirectoryKey, alg.settings.value(useDirectoryKey, useDirectoryDefault))
    }

    function updateSettings(settings_name, value) {
      settings[settings_name] = value
    }

    function emit() {
      alg.settings.setValue(intervalKey, settings[intervalKey])
      alg.settings.setValue(filesNumberKey, settings[filesNumberKey])
      alg.settings.setValue(snoozeKey, settings[snoozeKey])
      alg.settings.setValue(warningTimeKey, settings[warningTimeKey])
      alg.settings.setValue(saveDirectoryKey, settings[saveDirectoryKey])
      alg.settings.setValue(useDirectoryKey, settings[useDirectoryKey])
      configurationChanged(
        settings[intervalKey] * 60, // minutes
        settings[filesNumberKey],
        settings[snoozeKey] * 60, // minutes
        settings[warningTimeKey],
        settings[useDirectoryKey] ? settings[saveDirectoryKey] : saveDirectoryDefault,
        settings[useDirectoryKey])
    }
  }

  AlgScrollView {
    id: scrollView;
    parent: root.contentItem
    anchors.fill: parent
    anchors.margins: 16

    ColumnLayout {
      Layout.preferredWidth: scrollView.viewportWidth
      spacing: AlgStyle.defaultSpacing

      Repeater {
        id: layoutInstantiator

        model: ListModel {
          id: model
        }

        delegate: AlgSlider {
          id: slider
          text: label
          minValue: min_value
          maxValue: max_value
          value: alg.settings.value(settings_name, default_value)
          // integers only
          stepSize: 1
          precision: 0
          Layout.fillWidth: true
          onRoundValueChanged: internal.updateSettings(settings_name, roundValue)
        }
      }

      ColumnLayout {
        Layout.fillWidth: true
        AlgCheckBox {
          id: saveDirectoryCheckBox
          text: qsTr("Always save in the following directory:")
          checked: alg.settings.value(internal.useDirectoryKey, internal.useDirectoryDefault)
          height: 16
          onCheckedChanged: internal.updateSettings(internal.useDirectoryKey, checked)
        }
        RowLayout {
          Layout.fillWidth: true
          AlgTextEdit {
            id: saveDirectoryLabel
            text: elideDelegate.elidedText
            selectByKeyboard: false
            selectByMouse: false
            property string fullPath: alg.settings.value(internal.saveDirectoryKey, internal.saveDirectoryDefault)
            readOnly: true
            enabled: saveDirectoryCheckBox.checked
            Layout.fillWidth: true
            onFullPathChanged: {
              internal.updateSettings(internal.saveDirectoryKey, fullPath)
              fileDialog.folder = fullPath
            }
            TextMetrics {
              id: elideDelegate
              elide: Qt.ElideMiddle
              text: saveDirectoryLabel.fullPath
              elideWidth: saveDirectoryLabel.width - saveDirectoryLabel.anchors.leftMargin - saveDirectoryLabel.anchors.rightMargin
              font: saveDirectoryLabel.font
            }
          }
          AlgButton {
            text: qsTr("Select directory")
            enabled: saveDirectoryCheckBox.checked
            onClicked: {
              fileDialog.open()
            }
          }
        }
      }
    }
  }

  FileDialog {
    id: fileDialog
    title: qsTr("Please choose a directory")
    folder: internal.saveDirectoryDefault
    selectFolder: true
    selectMultiple: false
    selectExisting: true
    onAccepted: {
      saveDirectoryLabel.fullPath = alg.fileIO.urlToLocalFile(fileUrl) + "/"
    }
  }
}
