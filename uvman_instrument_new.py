from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QDialog
from datetime import datetime
from uvman_uvlog import UVLog

class UVManInstrumentNew(QDialog):
    def __init__(self, parent):
        super(UVManInstrumentNew, self).__init__(parent)    

        self.parent = parent
        self.settings = self.parent.settings        
        self.models = parent.models
        self.ui = uic.loadUi('uvman_instrument_new.ui', self)                 

        self.ui.cboxStation.setModel(self.models.station)
        viewColumn = self.models.station.fieldIndex('label')
        self.ui.cboxStation.setModelColumn(viewColumn)        
        self.ui.dtLastCalibrated.setDateTime(datetime.now())

    def accept(self):   
        try:     
            id, name, stationID, active, principal, model, channelCount, lastCalibrated = 0, '', 0, False, False, '', 0, datetime.now()
            fetchModule, validateModule, storeModule, matchExpression, comment = '', '', '', '', ''

            if not self.ui.editID.text():
                UVLog.show_error("Missing ID for new instrument")
                return
            id = self.ui.editID.text()

            if not self.ui.editName.text():
                UVLog.show_error("Missing name for new instrument")
                return
            name = self.ui.editName.text()
            
            stationIndex = self.models.station.index(self.cboxStation.currentIndex(), self.models.station.fieldIndex("id"))
            stationID = self.models.station.data(stationIndex)            
            if not stationID:
                UVLog.show_error("Missing station ID for new instrument")
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

            if principal:         
                conn = QSqlDatabase.database("query")       
                conn.transaction()
                query = QSqlQuery(conn)
                if not query.exec("update instrument set principal = 0 where id <> %s and station_id = %d" % (id, stationID)):
                    conn.rollback()
                    raise Exception("Unable to disable other principals for instrument %s" % (id)) 
                conn.commit()

            minst = self.models.instrument
            row = minst.rowCount()
            minst.insertRow(row)
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
            minst.setData(minst.index(row, 12), comment)
            if not minst.submitAll():
                minst.revertAll()
                UVLog.show_error("Unable to create instrument " + name)
                return            
            minst.select()
            self.close()
        except Exception as ex:
            UVLog.show_error(str(ex), True)