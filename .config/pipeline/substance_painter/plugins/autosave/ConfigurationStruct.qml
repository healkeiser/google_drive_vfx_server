import QtQuick 2.7

QtObject
{
  id: config
  property int interval: 0
  property int filesNumber: 0
  property int actualFileIndex: 0
  property int snooze: 0
  property int warningTime: 0
  property int remainingTime: 0
  property string tempFileName: ""
  property string saveDirectoryPath: ""
  property bool alwaysUseSaveDirectory: false
}
