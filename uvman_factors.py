from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from uvman_delegates import ChannelFormatDelegate
from uvman_uvlog import UVLog

class UVMAN_Factors():
    def __init__(self, parent):        
        self.settings = parent.settings
        self.parent = parent
        self.ui = self.parent.ui
        self.instrumentModel = self.parent.models.instrument
        self.productModel = self.parent.models.product
        self.channelFormat_delegate = ChannelFormatDelegate()        

    def onSelectFactors(self):               
        try:
            instrumentIndex = self.instrumentModel.index(self.ui.cboxFactorsInstruments.currentIndex(), self.instrumentModel.fieldIndex("id"))
            instrumentID = self.instrumentModel.data(instrumentIndex)            
            productIndex = self.productModel.index(self.ui.cboxFactorsProducts.currentIndex(), self.productModel.fieldIndex("id"))
            productID = self.productModel.data(productIndex)

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
