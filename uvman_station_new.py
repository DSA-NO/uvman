from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from uvman_uvlog import UVLog

class UVManStationNew(QDialog):
    def __init__(self, parent):
        super(UVManStationNew, self).__init__(parent)    

        self.parent = parent
        self.settings = self.parent.settings
        self.models = self.parent.models

        self.ui = uic.loadUi('uvman_station_new.ui', self)         

    def accept(self):   
        try:     
            name, active, latitude, longitude, comment = '', False, 0, 0, ''
            ftpHost, ftpUser, ftpPassword, ftpRemoteDir, ftpLocalDir, ftpPassiveMode = '', '', '', '', '', True

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

            ftpPassiveMode = self.ui.cbFTPPassiveMode.isChecked()
            
            if self.ui.editComment.text():
                comment = self.ui.editComment.text()

            UVLog.show_message("Creating new station " + name)    

            mstat = self.models.station
            row = mstat.rowCount()
            mstat.insertRow(row)
            mstat.setData(mstat.index(row, 1), name)
            mstat.setData(mstat.index(row, 2), active)
            mstat.setData(mstat.index(row, 3), latitude)
            mstat.setData(mstat.index(row, 4), longitude)
            mstat.setData(mstat.index(row, 5), ftpHost)
            mstat.setData(mstat.index(row, 6), ftpUser)
            mstat.setData(mstat.index(row, 7), ftpPassword)
            mstat.setData(mstat.index(row, 8), ftpRemoteDir)
            mstat.setData(mstat.index(row, 9), ftpLocalDir)            
            mstat.setData(mstat.index(row, 10), comment)
            mstat.setData(mstat.index(row, 11), ftpPassiveMode)
            if not mstat.submitAll():
                mstat.revertAll()
                UVLog.show_error("Unable to create station " + name)
                return
            mstat.select()
            self.close() 
        except Exception as ex:
            UVLog.show_error(str(ex), True)
