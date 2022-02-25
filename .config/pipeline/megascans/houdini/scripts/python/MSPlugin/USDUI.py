
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

class USDOptions(QtWidgets.QWidget):
    def __init__(self, usdOptions, settingsCallback):
        super(USDOptions, self).__init__()
        self.usdOptions = usdOptions
        self.settingsCallback = settingsCallback
        
        self.SetupOptionsW()


    def SetupOptionsW(self):
        self.widgetVBLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.widgetVBLayout)

        self.uiBox = QtWidgets.QGroupBox("USD Options :")        
        self.widgetVBLayout.addWidget(self.uiBox)        

        # Main UI Layout
        self.uiLayout = QtWidgets.QGridLayout()
        self.uiBox.setLayout(self.uiLayout)
        

        # Material type
        materialTypeText = QtWidgets.QLabel("USD Material")
        self.materialTypeDrop = QtWidgets.QComboBox()
        self.materialTypeDrop.setToolTip("Material type to create on USD stage")
        self.uiLayout.addWidget(materialTypeText, 0,0)
        self.uiLayout.addWidget(self.materialTypeDrop, 0, 1)
        usdMaterials = ["Karma", "Renderman", "Arnold"]
        self.materialTypeDrop.addItems(usdMaterials)

        if self.usdOptions["USDMaterial"] in usdMaterials:
            materialIndex = self.materialTypeDrop.findText(self.usdOptions["USDMaterial"])
            if materialIndex >= 0:
                self.materialTypeDrop.setCurrentIndex(materialIndex)

        self.materialTypeDrop.currentIndexChanged.connect(self.materialChanged)

        self.refpathRegexp = QtCore.QRegExp("[\\/][A-Za-z0-9\\/]+[\\/]")
        refpathValidator = QtGui.QRegExpValidator(self.refpathRegexp)
        # 3D Assets reference location
        # ref3DPathTag = "RefPath3D"
        # asset3dRefLabel = QtWidgets.QLabel("3D Assets Reference Path ")
        # asset3dRefPath = QtWidgets.QLineEdit()
        # asset3dRefPath.setObjectName(ref3DPathTag)
        # self.uiLayout.addWidget(asset3dRefLabel, 1,0)
        # self.uiLayout.addWidget(asset3dRefPath, 1,1)
        # asset3dRefPath.setValidator(refpathValidator)
        # asset3dRefPath.textEdited.connect(lambda : self.textInputChanged(asset3dRefPath))
        # asset3dRefPath.setText(self.usdOptions[ref3DPathTag])

        # 3D Plants reference location
        # ref3DPlantPathTag = "RefPath3DPlant"
        # plantsRefLabel = QtWidgets.QLabel("3D Plants Reference Path ")
        # plantsRefPath = QtWidgets.QLineEdit()
        # plantsRefPath.setObjectName(ref3DPlantPathTag)
        # self.uiLayout.addWidget(plantsRefLabel, 2,0)
        # self.uiLayout.addWidget(plantsRefPath, 2,1)
        # plantsRefPath.setValidator(refpathValidator)
        # plantsRefPath.textEdited.connect(lambda : self.textInputChanged(plantsRefPath))
        # plantsRefPath.setText(self.usdOptions[ref3DPlantPathTag])

        # Surfaces reference location
        # refSurfacePathTag = "RefPathSurface"
        # surfacesRefLabel = QtWidgets.QLabel("Surfaces Reference Path ")
        # surfacesRefPath = QtWidgets.QLineEdit()
        # surfacesRefPath.setObjectName(refSurfacePathTag)

        # self.uiLayout.addWidget(surfacesRefLabel, 3,0)
        # self.uiLayout.addWidget(surfacesRefPath, 3,1)
        # surfacesRefPath.editingFinished.connect(lambda : self.textInputChanged(surfacesRefPath))
        # surfacesRefPath.setText(self.usdOptions[refSurfacePathTag])

        # LODs as VariantSets
        # lodsVariantCheck = QtWidgets.QCheckBox("Import LODS as Variants")
        # lodsVariantCheck.setObjectName("ImportLods")
        # self.uiLayout.addWidget(lodsVariantCheck, 6,0 )
        # lodsVariantCheck.setChecked(self.usdOptions["ImportLods"])
        # lodsVariantCheck.toggled.connect(lambda state: self.miscOptionChanged(lodsVariantCheck,state))

    def miscOptionChanged(self, optionObject, state):
        optionName = optionObject.objectName()        
        self.usdOptions[optionName] = state
        self.settingsChanged()

    def materialChanged(self, index):
        self.usdOptions["USDMaterial"] = self.materialTypeDrop.itemText(index)
        self.settingsChanged()


    def textInputChanged(self, optionObject):        
        if optionObject.text() == self.usdOptions[optionObject.objectName()]:          
            return

        if self.refpathRegexp.exactMatch(optionObject.text()):
            optionObject.setStyleSheet("border: 1px solid black")
            self.usdOptions[optionObject.objectName()] = optionObject.text()
            self.settingsChanged()
        
        else:
            optionObject.setStyleSheet("border: 1px solid red")          


    def settingsChanged(self):
        
        self.settingsCallback("USDOptions", self.usdOptions)

