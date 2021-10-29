from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from uvman_uvlog import UVLog

class UVManStationEdit(QDialog):
    def __init__(self, parent, index, model):
        super(UVManStationEdit, self).__init__(parent)    

        self.ui = uic.loadUi('uvman_station_edit.ui', self)    
        self.settings = parent.settings
        self.index = index
        self.model = model

        record = self.model.record(self.index.row())
        self.ui.editName.setText(record.value(1))        
        self.ui.cbActive.setChecked(record.value(2))
        self.ui.editLatitude.setText(str(record.value(3)))
        self.ui.editLongitude.setText(str(record.value(4)))
        self.ui.editFTPHost.setText(record.value(5))
        self.ui.editFTPUser.setText(record.value(6))
        self.ui.editFTPPassword.setText(record.value(7))
        self.ui.editFTPRemoteDir.setText(record.value(8))
        self.ui.editFTPLocalDir.setText(record.value(9))
        self.ui.editComment.setText(record.value(10))        

    def accept(self):   
        try:     
            name, active, latitude, longitude, comment = '', False, 0, 0, ''
            ftpHost, ftpUser, ftpPassword, ftpRemoteDir, ftpLocalDir = '', '', '', '', ''

            if not self.ui.editName.text():
                UVLog.show_error("Missing name for new station")
                return

            name = self.ui.editName.text()

            active = self.ui.cbActive.isChecked()            

            if self.ui.editLatitude.text():
                latitude = float(self.ui.editLatitude.text())

            if self.ui.editLongitude.text():
                longitude = float(self.ui.editLongitude.text())
            
            if self.ui.editFTPHost.text():
                ftpHost = self.ui.editFTPHost.text()

            if self.ui.editFTPUser.text():
                ftpUser = self.ui.editFTPUser.text()

            if self.ui.editFTPPassword.text():
                ftpPassword = self.ui.editFTPPassword.text()

            if self.ui.editFTPRemoteDir.text():
                ftpRemoteDir = self.ui.editFTPRemoteDir.text()

            if self.ui.editFTPLocalDir.text():
                ftpLocalDir = self.ui.editFTPLocalDir.text()

            if self.ui.editComment.text():
                comment = self.ui.editComment.text()

            #_log.info("Updating station " + name)    
            UVLog.show_message("Updating station " + name)
            
            row = self.index.row()            
            self.model.setData(self.model.index(row, 1), name)
            self.model.setData(self.model.index(row, 2), active)
            self.model.setData(self.model.index(row, 3), latitude)
            self.model.setData(self.model.index(row, 4), longitude)
            self.model.setData(self.model.index(row, 5), ftpHost)
            self.model.setData(self.model.index(row, 6), ftpUser)
            self.model.setData(self.model.index(row, 7), ftpPassword)
            self.model.setData(self.model.index(row, 8), ftpRemoteDir)
            self.model.setData(self.model.index(row, 9), ftpLocalDir)
            self.model.setData(self.model.index(row, 10), comment)
            if not self.model.submitAll():
                self.model.revertAll()
                UVLog.show_error("Unable to update station " + name)
                return
            self.model.select()
            self.close() 
        except Exception as ex:
            UVLog.show_error(str(ex), True)