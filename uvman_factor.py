# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QTableWidgetItem
from uvman_delegate import ChannelFormatDelegate
from uvman_factor_new import UVManFactorNew
from uvman_factor_edit import UVManFactorEdit
from uvman_uvlog import UVLog

class UVMAN_Factor():
    def __init__(self, parent):        
        self.parent = parent
        self.settings = parent.settings        
        self.ui = self.parent.ui
        self.models = self.parent.models        
        self.channelFormat_delegate = ChannelFormatDelegate()  

        self.ui.cboxFactorsInstruments.setModel(self.models.instrument)
        viewColumn = self.models.instrument.fieldIndex('id')
        self.ui.cboxFactorsInstruments.setModelColumn(viewColumn)

        self.ui.cboxFactorsProducts.setModel(self.models.product)
        viewColumn = self.models.product.fieldIndex('label')
        self.ui.cboxFactorsProducts.setModelColumn(viewColumn)
        
        self.ui.cboxFactorsInstruments.currentIndexChanged.connect(self.onSelectFactor)
        self.ui.cboxFactorsProducts.currentIndexChanged.connect(self.onSelectFactor)  

        self.ui.btnFactorsNew.clicked.connect(self.onNew)            
        self.ui.btnFactorsEdit.clicked.connect(self.onEdit)            

    def onSelectFactor(self):               
        try:
            instrumentIndex = self.models.instrument.index(self.ui.cboxFactorsInstruments.currentIndex(), self.models.instrument.fieldIndex("id"))
            instrumentID = self.models.instrument.data(instrumentIndex)            
            productIndex = self.models.product.index(self.ui.cboxFactorsProducts.currentIndex(), self.models.product.fieldIndex("id"))
            productID = self.models.product.data(productIndex)

            conn = QSqlDatabase.database('query')
            query = QSqlQuery(conn)        
            success = query.exec("""
                select * 
                from guvfactor
                where instrument_id = %d and factortype_id = %d order by valid_from asc""" % (instrumentID, productID))
            if not success:
                self.log.error("Query failed: " + conn.lastError().text())
                return 
            self.ui.tblFactors.setRowCount(0)
            while query.next():
                rowPosition = self.ui.tblFactors.rowCount()
                self.ui.tblFactors.insertRow(rowPosition)            
                self.ui.tblFactors.setItem(rowPosition, 0, QTableWidgetItem(query.value("valid_from").toString("yyyy-MM-dd hh:mm:ss")))
                self.ui.tblFactors.setItem(rowPosition, 1, QTableWidgetItem(query.value("valid_to").toString("yyyy-MM-dd hh:mm:ss")))
                self.ui.tblFactors.setItem(rowPosition, 2, QTableWidgetItem(str(query.value("cie305"))))
                self.ui.tblFactors.setItem(rowPosition, 3, QTableWidgetItem(str(query.value("cie313"))))
                self.ui.tblFactors.setItem(rowPosition, 4, QTableWidgetItem(str(query.value("cie320"))))
                self.ui.tblFactors.setItem(rowPosition, 5, QTableWidgetItem(str(query.value("cie340"))))
                self.ui.tblFactors.setItem(rowPosition, 6, QTableWidgetItem(str(query.value("cie380"))))
                self.ui.tblFactors.setItem(rowPosition, 7, QTableWidgetItem(str(query.value("cie395"))))
                self.ui.tblFactors.setItem(rowPosition, 8, QTableWidgetItem(str(query.value("cie412"))))
                self.ui.tblFactors.setItem(rowPosition, 9, QTableWidgetItem(str(query.value("cie443"))))
                self.ui.tblFactors.setItem(rowPosition, 10, QTableWidgetItem(str(query.value("cie490"))))
                self.ui.tblFactors.setItem(rowPosition, 11, QTableWidgetItem(str(query.value("cie532"))))
                self.ui.tblFactors.setItem(rowPosition, 12, QTableWidgetItem(str(query.value("cie555"))))
                self.ui.tblFactors.setItem(rowPosition, 13, QTableWidgetItem(str(query.value("cie665"))))
                self.ui.tblFactors.setItem(rowPosition, 14, QTableWidgetItem(str(query.value("cie780"))))
                self.ui.tblFactors.setItem(rowPosition, 15, QTableWidgetItem(str(query.value("cie875"))))
                self.ui.tblFactors.setItem(rowPosition, 16, QTableWidgetItem(str(query.value("cie940"))))
                self.ui.tblFactors.setItem(rowPosition, 17, QTableWidgetItem(str(query.value("cie1020"))))
                self.ui.tblFactors.setItem(rowPosition, 18, QTableWidgetItem(str(query.value("cie1245"))))
                self.ui.tblFactors.setItem(rowPosition, 19, QTableWidgetItem(str(query.value("cie1640"))))
                self.ui.tblFactors.setItem(rowPosition, 20, QTableWidgetItem(str(query.value("par"))))                
                
                for i in range(2, 21):
                    self.ui.tblFactors.setItemDelegateForColumn(i, self.channelFormat_delegate)
            
            UVLog.show_message("Showing %d factors" % (self.ui.tblFactors.rowCount()))

        except Exception as ex:
            UVLog.show_error(str(ex), True)

    def onNew(self):  
        instrumentIndex = self.models.instrument.index(self.ui.cboxFactorsInstruments.currentIndex(), self.models.instrument.fieldIndex("id"))
        instrumentID = self.models.instrument.data(instrumentIndex)            
        productIndex = self.models.product.index(self.ui.cboxFactorsProducts.currentIndex(), self.models.product.fieldIndex("id"))
        productID = self.models.product.data(productIndex)  
        dlg = UVManFactorNew(self.parent, instrumentID, productID)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()        
        if dlg.getRefresh():
            self.onSelectFactor()

    def onEdit(self):  
        instrumentIndex = self.models.instrument.index(self.ui.cboxFactorsInstruments.currentIndex(), self.models.instrument.fieldIndex("id"))
        instrumentID = self.models.instrument.data(instrumentIndex)            
        productIndex = self.models.product.index(self.ui.cboxFactorsProducts.currentIndex(), self.models.product.fieldIndex("id"))
        productID = self.models.product.data(productIndex)  

        index = self.ui.tblFactors.currentIndex()
        if not index.isValid():        
            UVLog.show_error("No row selected")
            return
        dlg = UVManFactorEdit(self.parent, instrumentID, productID, index)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()        
        if dlg.getRefresh():
            self.onSelectFactor()