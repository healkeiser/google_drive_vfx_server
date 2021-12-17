import QtQuick 2.7
import Painter 1.0

PainterPlugin
{
	tickIntervalMS: -1 // Disabled, no need for Tick
	jsonServerPort: -1 // Disabled, no need for JSON server
	
	ResourceUpdaterWindow
	{
		id: window
	}
	
	Component.onCompleted:
	{
		var qmlToolbar = alg.ui.addWidgetToPluginToolBar( "toolbar.qml" )
		qmlToolbar.windowReference = window
	}
	
	onNewProjectCreated:
	{
		window.refreshInterface()
	}

	onProjectOpened:
	{
		window.refreshInterface()
	}
	
	onProjectAboutToClose:
	{
		window.refreshInterface()
	}
}
