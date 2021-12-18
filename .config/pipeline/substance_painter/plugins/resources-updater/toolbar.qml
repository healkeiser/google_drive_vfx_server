import AlgWidgets 2.0
import AlgWidgets.Style 2.0

AlgToolBarButton
{
	iconName: "ressources_updater.svg"
	tooltip: qsTr("Resources updater")

	property var windowReference : null

	onClicked:
	{
		try
		{
			windowReference.visible = true
			windowReference.refreshInterface()
			windowReference.raise()
			windowReference.requestActivate()
		}
		catch(err)
		{
			alg.log.exception(err)
		}
	}
}
