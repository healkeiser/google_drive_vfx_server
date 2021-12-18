pragma Singleton
import QtQuick 2.7

QtObject {
	readonly property QtObject window: QtObject {
		readonly property int width: 750
		readonly property int height: 500
		readonly property int minimumWidth: 450
		readonly property int minimumHeight: 300
	}

	readonly property QtObject widgets: QtObject {
		readonly property int barHeight: 30
		readonly property int resourceItemHeight: 80
		readonly property int buttonWidth: 100
	}

	readonly property int margin: 8
	readonly property int borderWidth: 2
	readonly property int radius: 4
}