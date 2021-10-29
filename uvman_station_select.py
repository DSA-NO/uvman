from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from uvman_uvlog import UVLog

class UVManStationSelect(QDialog):
    def __init__(self, parent, model):
        super().__init__(parent)    

        self.ui = uic.loadUi('uvman_station_select.ui', self)         
        self.model = model        
        self.ui.cboxStations.setModel(self.model)
        viewColumn = self.model.fieldIndex('label')
        self.ui.cboxStations.setModelColumn(viewColumn)                
        self.selectedStationID = None

    def accept(self):   
        try:                             
            stationIndex = self.model.index(self.cboxStations.currentIndex(), self.model.fieldIndex("id"))
            self.selectedStationID = self.model.data(stationIndex)            
            if not self.selectedStationID:
                UVLog.show_error("Missing station ID for select station")
                return
            
            self.done(QDialog.Accepted)            

        except Exception as ex:
            UVLog.show_error(str(ex), True)