# -*- coding: utf-8 -*-

from uvman_uvlog import UVLog
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QAbstractItemView
from uvman_instrument_new import UVManInstrumentNew
from uvman_instrument_edit import UVManInstrumentEdit

class UVMAN_Instrument():
    def __init__(self, parent):
        self.parent = parent
        self.settings = self.parent.settings        
        self.ui = self.parent.ui         
        self.models = self.parent.models

        self.ui.tblInstruments.setModel(self.models.instrument)
        self.ui.tblInstruments.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.ui.tblInstruments.setItemDelegate(QSqlRelationalDelegate(self.ui.tblInstruments))        
        header = self.ui.tblInstruments.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)       
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignLeft)  

        self.ui.btnInstrumentNew.clicked.connect(self.onNew)
        self.ui.btnInstrumentEdit.clicked.connect(self.onEdit)
        self.ui.btnInstrumentDelete.clicked.connect(self.onDelete)                

    def onNew(self):    
        dlg = UVManInstrumentNew(self, self.models.instrument, self.models.station)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()        

    def onEdit(self):    
        index = self.ui.tblInstruments.currentIndex()
        if not index.isValid():            
            UVLog.show_error("No row selected")
            return
        dlg = UVManInstrumentEdit(self, index, self.models.instrument, self.models.station)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()        

    def onDelete(self):               
        index = self.ui.tblInstruments.currentIndex()
        if not index.isValid():            
            UVLog.show_error("No row selected")
            return
        record = self.models.instrument.record(index.row())
        name = record.value(1)        
        if (QMessageBox.question(self, "Confirmation", ("Delete {0} from instruments?".format(name)), QMessageBox.Yes | QMessageBox.No) == QMessageBox.No):
            return
        self.models.instrument.removeRow(index.row())                
        if not self.models.instrument.submitAll():
            self.models.instrument.revertAll()            
            UVLog.show_error("Unable to remove instrument " + name)        
            return
        self.models.instrument.select()        
        UVLog.show_message("Instrument " + name + " deleted")