import QtQuick 2.7
import QtQuick.Window 2.2
import AlgWidgets 2.0
import AlgWidgets.Style 2.0


AlgToolBarButton
{
  id: root
  enabled: progressBar.value!=0
  iconName: "icon_hourglass.svg"
  tooltip: qsTr("Snooze autosave")
  
  property bool saving: false
  property bool startProgress: false
  property int remainingTime: 0
  property alias progressMaxValue: progressBar.to
  property bool active: true

  Rectangle
  {
    id: progressBar
    parent: background
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.bottom: parent.bottom
    height: width * value
    property real to: 1
    property real value: startProgress && active ? remainingTime / to : 0
    color: root.hovered ?
      Qt.rgba(0.133, 0.498, 0.427, 1.0) :
      Qt.rgba(0.184, 0.698, 0.612, 1.0)
  }
}