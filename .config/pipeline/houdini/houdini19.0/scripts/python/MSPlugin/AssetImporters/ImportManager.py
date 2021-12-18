
class ImportManager:
    def __init__(self):
        self.assetImporters = {}
        

    def registerImporter(self, importType, importer):
        self.assetImporters[importType] = importer

    def importAsset(self, assetData, importOptions, importParams):
        self.assetImporters[assetData["type"]].importAsset(assetData, importOptions, importParams)