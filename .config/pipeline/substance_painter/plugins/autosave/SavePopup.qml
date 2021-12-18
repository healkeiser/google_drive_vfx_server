import QtQuick 2.7
import QtQuick.Layouts 1.3
import AlgWidgets 2.0
import AlgWidgets.Style 2.0

AlgWindow {
  id: popup
  flags: Qt.Window
          | Qt.MSWindowsFixedSizeDialogHint
          | Qt.CustomizeWindowHint
          | Qt.WindowTitleHint
  modality: Qt.ApplicationModal
  title: qsTr("Saving...")
  width: 200
  height: contentLayout.height + 2 * internal.layoutMargins

  QtObject {
    id: internal
    readonly property int layoutMargins: 8
  }

  // overload close method
  function close() {
    // do nothing, the window is not supposed to be closed
  }

  ColumnLayout {
    id: contentLayout
    anchors.top: parent.top
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.margins: internal.layoutMargins
    spacing: AlgStyle.defaultSpacing

    AlgLabel {
      text: qsTr("Saving...")
    }
    AlgProgressBar {
      indeterminate: true
      Layout.fillWidth: true
    }
  }
}
