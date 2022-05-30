from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QDialog
from datetime import datetime
from uvman_uvlog import UVLog

class UVManInstrumentEdit(QDialog):
    def __init__(self, parent, index):
        super(UVManInstrumentEdit, self).__init__(parent)    

        self.parent = parent
        self.settings = self.parent.settings
        self.models = self.parent.models        
        self.index = index        
        self.ui = uic.loadUi('uvman_instrument_edit.ui', self)                   

        self.ui.cboxStation.setModel(self.models.station)
        viewColumn = self.models.station.fieldIndex('label')
        self.ui.cboxStation.setModelColumn(viewColumn)  

        record = self.models.instrument.record(self.index.row())      

        self.ui.editID.setText(str(record.value(0)))
        self.ui.editName.setText(str(record.value(1)))        
        self.ui.cboxStation.setCurrentText(record.value(2))        
        self.ui.cbActive.setChecked(record.value(3))
        self.ui.cbPrincipal.setChecked(record.value(4))
        self.ui.editModel.setText(record.value(5))
        self.ui.editChannelCount.setText(str(record.value(6)))
        self.ui.dtLastCalibrated.setDateTime(record.value(7))
        self.ui.editFetchModule.setText(record.value(8))
        self.ui.editValidateModule.setText(record.value(9))
        self.ui.editStoreModule.setText(record.value(10))
        self.ui.editMatchExpression.setText(record.value(11))        
        self.ui.editComment.setText(record.value(12))

    def accept(self):   
        try:     
            id, name, stationID, active, principal, model, channelCount, lastCalibrated = 0, '', 0, False, False, '', 0, datetime.now()
            fetchModule, validateModule, storeModule, matchExpression, comment = '', '', '', '', ''

            if not self.ui.editID.text():
                UVLog.show_error("Missing ID for instrument")
                return
            id = self.ui.editID.text()

            if not self.ui.editName.text():
                UVLog.show_error("Missing name for instrument")
                return
            name = self.ui.editName.text()
            
            stationIndex = self.models.station.index(self.cboxStation.currentIndex(), self.models.station.fieldIndex("id"))
            stationID = self.models.station.data(stationIndex)            
            if not stationID:
                UVLog.show_error("Missing station ID for instrument")
                return

            active = self.ui.cbActive.isChecked()
            principal = self.ui.cbPrincipal.isChecked()
            model = self.ui.editModel.text()
            channelCount = int(self.ui.editChannelCount.text())
            lastCalibrated = self.ui.dtLastCalibrated.dateTime()
            fetchModule = self.ui.editFetchModule.text()
            validateModule = self.ui.editValidateModule.text()
            storeModule = self.ui.editStoreModule.text()
            matchExpression = self.ui.editMatchExpression.text()            
            comment = self.ui.editComment.text()
            
            UVLog.show_message("Updating instrument " + name)    
            
            if principal:
                conn = QSqlDatabase.database('query')
                conn.transaction()
                query = QSqlQuery(conn)
                if not query.exec("update instrument set principal = 0 where id <> %s and station_id = %d" % (id, stationID)):
                    conn.rollback()
                    raise Exception("Unable to disable other principals for instrument %s" % (id)) 
                conn.commit()

            row = self.index.row()
            minst = self.models.instrument
            minst.setData(minst.index(row, 0), id)
            minst.setData(minst.index(row, 1), name)
            minst.setData(minst.index(row, 2), stationID)
            minst.setData(minst.index(row, 3), active)
            minst.setData(minst.index(row, 4), principal)
            minst.setData(minst.index(row, 5), model)
            minst.setData(minst.index(row, 6), channelCount)
            minst.setData(minst.index(row, 7), lastCalibrated)
            minst.setData(minst.index(row, 8), fetchModule)
            minst.setData(minst.index(row, 9), validateModule)
            minst.setData(minst.index(row, 10), storeModule)
            minst.setData(minst.index(row, 11), matchExpression)            
            minst.setData(minst.index(row, 14), comment)
            if not minst.submitAll():                    
                minst.revertAll()
                raise Exception("Unable to update instrument %s" % (id))       
            minst.select()
            self.close()                    
        except Exception as ex:
            UVLog.show_error(str(ex), True)