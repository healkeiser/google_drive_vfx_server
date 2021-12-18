import QtQuick 2.7
import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import AlgWidgets 2.0
import AlgWidgets.Style 2.0
import "."

AlgWindow
{
	id: window
	title: qsTr("Substance 3D Painter - Resources Updater")
	visible: false
	width: Style.window.width
	height: Style.window.height
	minimumWidth: Style.window.minimumWidth
	minimumHeight: Style.window.minimumHeight
	
	//Flags to keep the window on top
	flags: Qt.Window
		| Qt.WindowTitleHint // title
		| Qt.WindowSystemMenuHint // Recquired to add buttons
		| Qt.WindowMinMaxButtonsHint // minimize and maximize button
		| Qt.WindowCloseButtonHint // close button


	ColumnLayout
	{
		id: horizontalLayout
		anchors.fill: parent
		spacing: 0

		Rectangle
		{
			id: titleBar
			Layout.fillWidth: true
			Layout.preferredHeight: Style.widgets.barHeight

			color: AlgStyle.colors.gray(10)

			RowLayout
			{
				anchors.fill: parent
				
				AlgLabel
				{
					id: projectName
					font.pixelSize: 14
					font.bold: true
					Layout.leftMargin: Style.margin
					
					text: qsTr("Project : ")
				}

				AlgButton
				{
					property bool pinState: false
					text: pinState ? qsTr("Unpin window") : qsTr("Pin window")
					Layout.alignment: Qt.AlignRight
					Layout.rightMargin: Style.margin
					Layout.preferredWidth: Style.widgets.buttonWidth
					
					onClicked:
					{
						pinState = !pinState
						
						if( pinState ) {
							// Add the flag "keep window on top"
							window.flags |= Qt.WindowStaysOnTopHint;
						} else {
							// Remove the flag "keep window on top"
							window.flags &= ~Qt.WindowStaysOnTopHint;
						}
					}
				}
			}
		}
		
		AlgTabBar
		{
			id: tabBar
			Layout.fillWidth: true
			Layout.preferredHeight: switchToResources.height

			AlgTabButton
			{
				id: switchToResources
				text: qsTr("Resources")
			}

			AlgTabButton
			{
				id: switchToShaders
				text: qsTr("Shaders")
			}
		}
		
		Rectangle
		{
			id: filteringBar
			Layout.fillWidth: true
			Layout.preferredHeight: Style.widgets.barHeight
			
			color: AlgStyle.background.color.mainWindow
			
			RowLayout
			{
				width: parent.width
				anchors {
					verticalCenter: parent.verticalCenter;
				}
				
				AlgLabel
				{
					Layout.leftMargin: Style.margin
					text: qsTr("Status : ")
				}
				
				AlgComboBox
				{
					id: statusFilter
					Layout.preferredWidth: Style.widgets.buttonWidth
					Layout.preferredHeight: textFilter.height

					model: [qsTr("All"), qsTr("Outdated"), qsTr("Non-Outdated")]

					onCurrentIndexChanged:
					{
						resourcesListView.current_filter = getFilterMode()
					}
				}
				
				AlgLabel
				{
					Layout.leftMargin: Style.margin
					text: qsTr("Name filter : ")
				}
				
				AlgTextInput
				{
					id: textFilter
					Layout.preferredWidth: Style.widgets.buttonWidth
					text: ""

					onTextChanged:
					{
						resourcesListView.filter_text = text
					}
				}
				
				AlgToolButton
				{
					iconName: AlgStyle.icons.datawidget.remove
					visible: textFilter.text !== ""
					
					onClicked:
					{
						textFilter.text = ""
					}
				}
				
				Item
				{
					Layout.fillWidth: true
				}
				
				AlgButton
				{
					text: qsTr("Top")
					Layout.preferredWidth: Style.widgets.buttonWidth/2
					
					onClicked:
					{
						resourcesListView.scrollResourcesListToTop()
					}
				}
				
				AlgButton
				{
					text: qsTr("Bottom")
					Layout.preferredWidth: Style.widgets.buttonWidth/2
					Layout.rightMargin: Style.margin
					
					onClicked:
					{
						resourcesListView.scrollResourcesListToBottom()
					}
				}
			}
		}

		ResourcesListView
		{
			id: resourcesListView
			currentMode: tabBar.currentIndex
		}
		
		Rectangle
		{
			Layout.fillWidth: true
			Layout.preferredHeight: Style.widgets.barHeight
			Layout.bottomMargin: Style.margin
			Layout.topMargin: Style.margin
			
			color: AlgStyle.background.color.mainWindow
			
			RowLayout
			{
				anchors.fill: parent
				
				AlgButton
				{
					text: qsTr("Refresh")
					Layout.leftMargin: Style.margin
					Layout.preferredHeight: 30
					
					onClicked:
					{
						refreshInterface()
					}
				}
				
				AlgLabel
				{
					id: infoResourcesCount
					Layout.fillWidth: true

					text: "(0 resources, 0 outdated)"
					opacity: 0.75
				}
				
				AlgButton
				{
					text: qsTr("Update All")
					Layout.preferredHeight: 30
					Layout.rightMargin: Style.margin
					
					onClicked:
					{
						resourcesListView.updateAllResources()
					}
				}
			}
		}
	}
	
	function getFilterMode() {
		switch(statusFilter.currentIndex) {
		case 0:
			return resourcesListView.filter_ALL
		case 1:
			return resourcesListView.filter_OUTDATED
		case 2:
			return resourcesListView.filter_NO_OUTDATED
		}
	}
	
	function refreshInterface() {
		try {
			if (!window.visible) {
				return
			}
			projectName.text = qsTr("Project : ")
			
			resourcesListView.updateResourcesList()
			resourcesListView.scrollResourcesListToTop()

		} catch(err) {
			alg.log.exception(err)
		}
	}
}
