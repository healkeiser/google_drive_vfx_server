from PySide2.QtWidgets import QVBoxLayout,QGroupBox,QGridLayout,QComboBox,QLabel,QCheckBox,QWidget,QFrame

from .Utilities.AssetData import *
import hou

from .MaterialsSetup.MaterialsCreator import MaterialsCreator

class UIOptions(QWidget):
    def __init__(self, importOptions, settingsCallback):
        super(UIOptions, self).__init__()
        self.supportedRenderers = ["Mantra", "Arnold", "Octane", "Redshift", "Renderman"]
        
        self.importOptions = importOptions
        self.settingsChanged = settingsCallback
        self.SetupOptionsW()
        
        


    def SetupOptionsW(self):
        self.matCreator = MaterialsCreator()
        # print(self.matCreator.materialMap)
        
        # self.uiSettings = loadUISettings("ImportOptions")   
        self.widgetVBLayout =QVBoxLayout()
        self.setLayout(self.widgetVBLayout)

        self.uiBox = QGroupBox("Import Options:")
        self.widgetVBLayout.addWidget(self.uiBox)

        # Main UI Layout
        uiBoxLayout = QVBoxLayout()
        self.uiBox.setLayout(uiBoxLayout)



        # Layout for misc options
        miscOptionsL = QGridLayout()
        uiBoxLayout.addLayout(miscOptionsL)

        # Renderer selection options
        renderBoxText = QLabel("Renderer :")
        
        miscOptionsL.addWidget(renderBoxText, 0,0)
        rendererList = self.getRendererList()       
        self.renderBoxInput = QComboBox()
        self.renderBoxInput.setToolTip("Currently selected Renderer")
        self.renderBoxInput.addItems(rendererList)

        if self.importOptions["Renderer"] in rendererList:
            rendererIndex = self.renderBoxInput.findText(self.importOptions["Renderer"])
            if rendererIndex >= 0:
                self.renderBoxInput.setCurrentIndex(rendererIndex)

        miscOptionsL.addWidget(self.renderBoxInput, 0 , 1)

        # Material selection option
        materialBoxText = QLabel("Material Type:")
        miscOptionsL.addWidget(materialBoxText, 1,0)

        self.materialBoxList = QComboBox()
        self.materialBoxList.setToolTip("Selected material type for the Renderer")
        miscOptionsL.addWidget(self.materialBoxList, 1,1)

        self.updateMaterialList(self.renderBoxInput.currentText())

        # UI Separator
        separatorFrame = QFrame()
        separatorFrame.setFrameShape(QFrame.HLine)
        separatorFrame.setFrameShadow(QFrame.Sunken)        
        miscOptionsL.addWidget(separatorFrame, 2,0, 1,2)
         

        # Misc option : Scattering node
        setupScatteringRadio = QCheckBox("Use Megascans Scattering")
        setupScatteringRadio.setToolTip("Setup Megascans scattering for 3D Assets")
        setupScatteringRadio.setObjectName("UseScattering")
        miscOptionsL.addWidget(setupScatteringRadio, 3, 0)
        setupScatteringRadio.setChecked(self.importOptions["UseScattering"])
        setupScatteringRadio.toggled.connect(lambda state: self.miscOptionChanged(setupScatteringRadio,state))


        # Misc option : Use EXR Displacmenet
        # useExrRadio = QCheckBox("Use EXR Displacement")
        # useExrRadio.setObjectName("UseExrDisplacement")
        # miscOptionsL.addWidget(useExrRadio, 3 , 1)
        # useExrRadio.setChecked(self.importOptions["UseExrDisplacement"])
        # useExrRadio.toggled.connect(lambda state: self.miscOptionChanged(useExrRadio,state))


        # Misc option : Mesh setup for Atlas
        useAtlasSplitterRadio = QCheckBox("Use Atlas Splitter")
        useAtlasSplitterRadio.setToolTip("Generate meshes for Atlas")
        useAtlasSplitterRadio.setObjectName("UseAtlasSplitter")
        miscOptionsL.addWidget(useAtlasSplitterRadio, 4,0)
        useAtlasSplitterRadio.setChecked(self.importOptions["UseAtlasSplitter"])
        useAtlasSplitterRadio.toggled.connect(lambda state: self.miscOptionChanged(useAtlasSplitterRadio,state))

        # Misc option : Enable LODs
        enableLodsRadio = QCheckBox("Enable LODs")
        enableLodsRadio.setToolTip("Import LODs for 3D Assets")
        enableLodsRadio.setObjectName("EnableLods")
        miscOptionsL.addWidget(enableLodsRadio, 3,1)
        enableLodsRadio.setChecked(self.importOptions["EnableLods"])
        enableLodsRadio.toggled.connect(lambda state: self.miscOptionChanged(enableLodsRadio,state))

        # Misc option : Enable Quixel Motion
        enableMotionCheck = QCheckBox("Apply Motion (Plants)")
        enableMotionCheck.setToolTip("Apply motion to 3D Plants")
        enableMotionCheck.setObjectName("ApplyMotion")
        miscOptionsL.addWidget(enableMotionCheck, 4,1)
        enableMotionCheck.setChecked(self.importOptions["ApplyMotion"])
        enableMotionCheck.toggled.connect(lambda state: self.miscOptionChanged(enableMotionCheck,state))

        # Misc option : Convert to RAT
        ratConvertCheck = QCheckBox("Convert To RAT")
        ratConvertCheck.setToolTip("Convert all textures to .RAT for Mantra and Karma")
        ratConvertCheck.setObjectName("ConvertToRAT")
        miscOptionsL.addWidget(ratConvertCheck, 5,0)
        ratConvertCheck.setChecked(self.importOptions["ConvertToRAT"])
        ratConvertCheck.toggled.connect(lambda state: self.miscOptionChanged(ratConvertCheck,state))

        # Enable USD Check
        # if EnableUSD() == True:
            # UI Separator
        separatorFrame2 = QFrame()
        separatorFrame2.setFrameShape(QFrame.HLine)
        separatorFrame2.setFrameShadow(QFrame.Sunken)        
        miscOptionsL.addWidget(separatorFrame2, 6,0, 1,2)

        self.usdCheck = QCheckBox("Import Assets on USD Stage")
        self.usdCheck.setToolTip("Import and setup assets in Solaris in Houdini 18.")
        self.usdCheck.setObjectName("EnableUSD")
        miscOptionsL.addWidget(self.usdCheck, 7,0,1,2)
        self.usdCheck.setChecked(self.importOptions["EnableUSD"])
        self.usdCheck.toggled.connect(lambda state: self.miscOptionChanged(self.usdCheck,state))

        if EnableUSD() == False:
            self.usdCheck.setEnabled(False)
            if self.importOptions["EnableUSD"] == True:
                self.usdCheck.setChecked(False)





        # Set values to settings

        # Connect change signals to slots
        self.renderBoxInput.currentIndexChanged.connect(self.RendererChanged)
        self.materialBoxList.currentIndexChanged.connect(self.MaterialTypeChanged)



    def miscOptionChanged(self, optionObject, state):
        optionName = optionObject.objectName()        
        self.importOptions[optionName] = state
        self.uiSettingsChanged()
    
    def RendererChanged(self, index):
        self.importOptions["Renderer"] = self.renderBoxInput.itemText(index)
        self.updateMaterialList(self.importOptions["Renderer"])
        self.uiSettingsChanged()

    def updateMaterialList(self, selectedRenderer):
        supportedMaterials = {"Mantra" : ["Principled Shader", "Triplanar"], "Renderman" : ["Pixar Surface"], "Redshift" : ["Redshift Textures", "Redshift Triplanar"]}
        supportedMaterials = {}
        rendererlist = self.getRendererList()
        for renderer in rendererlist:
            supportedMaterials[renderer] = []
            rendererMaterials = self.matCreator.materialMap[renderer]
            for matType in rendererMaterials.keys():
                supportedMaterials[renderer].append(matType)

        rendererMaterials = supportedMaterials[selectedRenderer]
        self.materialBoxList.clear()   
        self.materialBoxList.addItems(rendererMaterials)        
        
        if self.importOptions["Material"] in rendererMaterials:
            materialIndex = self.materialBoxList.findText(self.importOptions["Material"])
            self.materialBoxList.setCurrentIndex(materialIndex)


    def MaterialTypeChanged(self, index):
        self.importOptions["Material"] = self.materialBoxList.itemText(index)
        self.uiSettingsChanged()

    def uiSettingsChanged(self):
        self.settingsChanged("ImportOptions", self.importOptions)

    def getRendererList(self):
        rendererList =[]
        registeredRenderers = self.matCreator.materialMap.keys()
        for renderer in registeredRenderers:
            if renderer == "Mantra":
                rendererList.append(renderer)

            if renderer == "Arnold" and "arnold" in hou.ropNodeTypeCategory().nodeTypes():
                rendererList.append(renderer)

            if renderer == "Redshift" and "Redshift_ROP" in hou.ropNodeTypeCategory().nodeTypes():
                rendererList.append(renderer)
                

            if renderer == "Octane" and "Octane_ROP" in hou.ropNodeTypeCategory().nodeTypes():
                rendererList.append(renderer)

            if renderer == "Renderman" and "ris" in hou.ropNodeTypeCategory().nodeTypes():
                rendererList.append(renderer)

        return rendererList

            
               

            


