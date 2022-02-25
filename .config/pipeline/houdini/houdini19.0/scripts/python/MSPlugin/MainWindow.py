from PySide2 import QtGui
from PySide2 import QtCore
from PySide2.QtWidgets import QLabel, QWidget,QApplication, QVBoxLayout,QMainWindow

import hou


from .OptionsUI import UIOptions
from .USDUI import USDOptions
from .SocketListener import QLiveLinkMonitor
from .MSImporter import MSImporter
from .Utilities.AssetData import *
from .Utilities.SettingsManager import SettingsManager

def GetHostApp():
    try:
        mainWindow =hou.ui.mainQtWindow()
        while True:
            lastWin = mainWindow.parent()
            if lastWin:
                mainWindow = lastWin
            else:
                break
        return mainWindow
    except:
        pass



class MSMainWindow(QMainWindow):
    # Singleton pattern for the class, ideal would be metaclass Singleton implementation
    __instance = None
    def __init__(self):        
        if MSMainWindow.__instance != None:
            return
        else:
            MSMainWindow.__instance = self
        super(MSMainWindow,self).__init__(GetHostApp())
        self.settingsManager = SettingsManager()
        self.uiSettings = self.settingsManager.getSettings()
        self.SetupMainWindow()
        self.setWindowTitle("Megascans Plugin")

        self.setFixedWidth(600)
        
        
    def getStylesheet(self):
        stylesheet_ = ("""

        QCheckBox { background: transparent; color: #E6E6E6; font-family: Source Sans Pro; font-size: 14px; }
        QCheckBox::indicator:hover { border: 2px solid #2B98F0; background-color: transparent; }
        QCheckBox::indicator:checked:hover { background-color: #2B98F0; border: 2px solid #73a5ce; }
        QCheckBox:indicator{ color: #67696a; background-color: transparent; border: 2px solid #67696a;
        width: 14px; height: 14px; border-radius: 2px; }
        QCheckBox::indicator:checked { border: 2px solid #18191b;
        background-color: #2B98F0; color: #ffffff; }
        QCheckBox::hover { spacing: 12px; background: transparent; color: #ffffff; }
        QCheckBox::checked { color: #ffffff; }
        QCheckBox::indicator:disabled, QRadioButton::indicator:disabled { border: 1px solid #444; }
        QCheckBox:disabled { background: transparent; color: #414141; font-family: Source Sans Pro;
        font-size: 14px; margin: 0px; text-align: center; }
       
        QComboBox { color: #FFFFFF; font-size: 14px; padding: 2px 2px 2px 8px; font-family: Source Sans Pro;
        selection-background-color: #1d1e1f; background-color: #1d1e1f; }

        QListView {padding: 4px;}
        QListView::item { margin: 4px; } 
      
        QComboBox:hover { color: #c9c9c9; font-size: 14px; padding: 2px 2px 2px 8px; font-family: Source Sans Pro;
        selection-background-color: #232426; background-color: #232426; } """)

        return stylesheet_
       

    def SetupMainWindow(self):
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)

        self.optionsUI = UIOptions(self.uiSettings["UI"]["ImportOptions"], self.uiSettingsChanged)
        self.windowLayout = QVBoxLayout()

        self.mainWidget.setLayout(self.windowLayout)
        self.windowLayout.addWidget(self.optionsUI)


        self.usdUI = USDOptions(self.uiSettings["UI"]["USDOptions"], self.uiSettingsChanged)
        self.windowLayout.addWidget(self.usdUI)
        
        if EnableUSD() == True:
            self.usdUI.setEnabled(True)
            

            if self.uiSettings["UI"]["ImportOptions"]["EnableUSD"]:
                self.usdUI.setEnabled(True)                
                self.usdEnabled = True
            else:
                self.usdUI.setEnabled(False)                
                self.usdEnabled = False
           
            self.optionsUI.usdCheck.stateChanged.connect(self.SettingsChanged)

        else:
            self.usdUI.setEnabled(False)
            self.style_ = ("""  QWidget { background-color: #353535; } """)
            self.setStyleSheet(self.style_)
        

    def SettingsChanged(self):
        if self.usdEnabled == True:
            self.usdEnabled = False                    
            # self.setFixedHeight(400)
            # self.usdUI.hide()
            self.usdUI.setEnabled(False)

        else:
            self.usdEnabled = True
            # self.setFixedHeight(500)
            # self.usdUI.show()
            self.usdUI.setEnabled(True)

        
        
        

    @staticmethod 
    def getInstance():        
        if MSMainWindow.__instance == None:
            MSMainWindow()
        return MSMainWindow.__instance

    def uiSettingsChanged(self, settingsKey, uiSettings):
        self.uiSettings["UI"][settingsKey] = uiSettings
        self.settingsManager.saveSettings(self.uiSettings)
        

    
def initializeWindow():
    mWindow = MSMainWindow.getInstance()
    mWindow.show()    

    if len(QLiveLinkMonitor.Instance) == 0:
        bridge_monitor = QLiveLinkMonitor()
        # LiveLinkUI.Thread_Monitor = QLiveLinkMonitor.Instance[0]
        # bridge_monitor.Bridge_Call.connect(bridge_monitor.InitializeImporter)
        bridge_monitor.Bridge_Call.connect(MSImporter.getInstance().importController)
        bridge_monitor.start()
    # else:
    #     LiveLinkUI.Thread_Monitor = QLiveLinkMonitor.Instance[0]





