import QtQuick 2.7
import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import AlgWidgets 2.0
import AlgWidgets.Style 2.0
import "."

AlgPopup
{
	id: resourceInfo
	width: parent.width
	height: scrollArea.viewportHeight
	parent: scrollArea
	visible:false
	
	Component.onCompleted:
	{
		background.color = AlgStyle.colors.gray(15)
		background.opacity = 0.8
	}
	
	//Allow to close the popup when clicking outside the
	//rectangle displaying the resource information.
	MouseArea
	{
		parent: resourceInfo.background
		anchors.fill: parent
		
		onClicked:
		{
			resourceInfo.close()
		}
	}
	
	Rectangle
	{
		anchors.centerIn: parent
		width: parent.width * 0.8
		height: content.height
		
		border.color: AlgStyle.colors.gray(30)
		border.width: Style.borderWidth
		radius: Style.radius

		color: AlgStyle.colors.gray(25)

		MouseArea
		{
			anchors.fill: parent
		}

		ColumnLayout
		{
			id: content
			anchors {
				left: parent.left
				right: parent.right
			}
			
			RowLayout
			{
				Layout.margins: Style.margin

				Image
				{
					id: thumbnail
					source: ""
					fillMode: Image.PreserveAspectFit
					mipmap: true
					Layout.preferredWidth: infosList.height
					Layout.preferredHeight: infosList.height
					sourceSize.width: 512
					sourceSize.height: 512
				}
				
				GridLayout
				{
					columns: 2
					id: infosList
					
					//---------------------------------
					// Name
					//---------------------------------
					AlgLabel
					{
						text: qsTr("Name : ")
						enabled: infoName.text !== ""
					}
					
					AlgLabel
					{
						id: infoName
						text: ""
						Layout.fillWidth: true
						elide: Text.ElideRight
					}
					
					
					//---------------------------------
					// Type
					//---------------------------------
					AlgLabel
					{
						text: qsTr("Type : ")
						enabled: infoType.text !== ""
					}
					
					AlgLabel
					{
						id: infoType
						text: ""
						Layout.fillWidth: true
						elide: Text.ElideRight
					}
					
					
					//---------------------------------
					// Shelf name
					//---------------------------------
					AlgLabel
					{
						text: qsTr("Shelf : ")
						enabled: infoShelf.text !== ""
					}
					
					AlgLabel
					{
						id: infoShelf
						text: ""
						Layout.fillWidth: true
						elide: Text.ElideRight
					}
					
					
					//---------------------------------
					// Location
					//---------------------------------
					AlgLabel
					{
						text: qsTr("Path : ")
						enabled: infoShelfPath.text !== ""
					}
					
					AlgLabel
					{
						id: infoShelfPath
						text: ""
						Layout.fillWidth: true
						elide: Text.ElideRight
					}
					
					
					//---------------------------------
					// Category
					//---------------------------------
					AlgLabel
					{
						text: qsTr("Category : ")
						enabled: infoCategory.text !== ""
					}
					
					AlgLabel
					{
						id: infoCategory
						text: ""
						Layout.fillWidth: true
						elide: Text.ElideRight
					}
					
					
					//---------------------------------
					// Tags
					//---------------------------------
					AlgLabel
					{
						text: qsTr("Tags : ")
						enabled: infoTags.text !== ""
					}
					
					AlgLabel
					{
						id: infoTags
						text: ""
						Layout.fillWidth: true
						elide: Text.ElideRight
					}
					
					
					//---------------------------------
					// Usages
					//---------------------------------
					AlgLabel
					{
						text: qsTr("Usages : ")
						enabled: infoUsages.text !== ""
					}
					
					AlgLabel
					{
						id: infoUsages
						text: ""
						Layout.fillWidth: true
						elide: Text.ElideRight
					}
					
					
					//---------------------------------
					// URL
					//---------------------------------
					AlgLabel
					{
						text: qsTr("Full URL : ")
						enabled: infoUrl.text !== ""
					}
					
					AlgLabel
					{
						id: infoUrl
						text: ""
						Layout.fillWidth: true
						elide: Text.ElideRight
					}
				}
				
			}
		}
	}

	function getInfoAboutResource(url) {
		try {
			var resInfo = alg.resources.getResourceInfo(url)

			infoName.text = resInfo.name !== undefined ?
				resInfo.name :
				""
			infoType.text = resInfo.type !== undefined ?
				resInfo.type :
				""
			infoShelf.text = resInfo.shelfName !== undefined ?
				resInfo.shelfName :
				""
			infoShelfPath.text = resInfo.shelfPath !== undefined ?
				resInfo.shelfPath :
				""
			infoCategory.text = resInfo.category !== undefined ?
				resInfo.category :
				""
			infoTags.text = resInfo.tags !== undefined ?
				resInfo.tags.toString() :
				""
			infoUsages.text = resInfo.usages !== undefined ?
				resInfo.usages.toString() :
				""
			infoUrl.text = url
			
			thumbnail.source = "image://resources/" + url
			
			//Display popup
			resourceInfo.visible = true
		} catch(err) {
			alg.log.exception(err)
		}
	}
}