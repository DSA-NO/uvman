# -*- coding: utf-8 -*-

from uvman_uvlog import UVLog
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QAbstractItemView
from uvman_delegate import PasswordDelegate
from uvman_station_new import UVManStationNew
from uvman_station_edit import UVManStationEdit

class UVMAN_Station():
    def __init__(self, parent):
        self.parent = parent
        self.settings = self.parent.settings        
        self.ui = self.parent.ui         
        self.models = self.parent.models 

        self.password_delegate = PasswordDelegate()        

        self.ui.tblStations.setModel(self.models.station)
        self.ui.tblStations.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.ui.tblStations.setStyleSheet("QHeaderView::section { background-color: rgba(0, 0, 255, 128) }")
        self.ui.tblStations.setItemDelegateForColumn(7, self.password_delegate)        
        header = self.ui.tblStations.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)       
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignLeft)

        self.ui.btnStationNew.clicked.connect(self.onNew)
        self.ui.btnStationEdit.clicked.connect(self.onEdit)
        self.ui.btnStationDelete.clicked.connect(self.onDelete)               

    def onNew(self):    
        dlg = UVManStationNew(self.parent)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()        

    def onEdit(self):    
        index = self.ui.tblStations.currentIndex()
        if not index.isValid():        
            UVLog.show_error("No row selected")
            return
        dlg = UVManStationEdit(self.parent, index)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()        

    def onDelete(self):               
        index = self.ui.tblStations.currentIndex()
        if not index.isValid():        
            UVLog.show_error("No row selected")
            return
        record = self.models.station.record(index.row())
        name = record.value(1)        
        if (QMessageBox.question(self.parent, "Confirmation", ("Delete {0} from stations?".format(name)), QMessageBox.Yes | QMessageBox.No) == QMessageBox.No):
            return
        self.models.station.removeRow(index.row())
        if not self.models.station.submitAll():
            self.models.station.revertAll()            
            UVLog.show_error("Unable to remove station " + name)        
            return
        self.models.station.select()
        UVLog.show_message("Station " + name + " deleted")    