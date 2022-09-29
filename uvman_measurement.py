from PyQt5.QtCore import QDateTime, Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from uvman_delegate import ChannelFormatDelegate
from uvman_uvlog import UVLog
from uvman_station_select import UVManStationSelect

class UVMAN_Measurement():
    def __init__(self, parent):
        self.parent = parent
        self.settings = self.parent.settings        
        self.ui = self.parent.ui
        self.models = self.parent.models        

        cdt = QDateTime.currentDateTime()
        self.ui.dtMeasurementsFrom.setDateTime(cdt.addDays(-1))
        self.ui.dtMeasurementsTo.setDateTime(cdt)

        self.channelFormat_delegate = ChannelFormatDelegate()

        self.ui.cboxMeasurementsStation.setModel(self.models.station)
        vcMeasurementsStation = self.models.station.fieldIndex('label')
        self.ui.cboxMeasurementsStation.setModelColumn(vcMeasurementsStation)          
        self.ui.btnMeasurementsStationClear.clicked.connect(self.onStationClear)      

        self.ui.cboxMeasurementsChannels.setModel(self.models.channel_count)                
        self.ui.btnMeasurementsChannelsClear.clicked.connect(self.onChannelsClear)      

        self.ui.cboxMeasurementsInstrument.setModel(self.models.instrument)
        vcMeasurementsInstrument = self.models.instrument.fieldIndex('id')
        self.ui.cboxMeasurementsInstrument.setModelColumn(vcMeasurementsInstrument)  
        self.ui.btnMeasurementsInstrumentClear.clicked.connect(self.onInstrumentClear)      

        header = self.ui.tblMeasurements.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)       
        #header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignLeft)                    

        self.ui.btnMeasurementsSearch.clicked.connect(self.onSearch)      
        self.ui.btnMeasurementsEnablePrincipal.clicked.connect(self.onEnablePrincipal)      
        self.ui.btnMeasurementsDisablePrincipal.clicked.connect(self.onDisablePrincipal)      
        self.ui.btnMeasurementsSetStation.clicked.connect(self.onSetStation)      
        self.ui.btnMeasurementsDelete.clicked.connect(self.onDelete)  

    def onStationClear(self):
        self.ui.cboxMeasurementsStation.setCurrentIndex(-1)

    def onChannelsClear(self):
        self.ui.cboxMeasurementsChannels.setCurrentIndex(-1)

    def onInstrumentClear(self):
        self.ui.cboxMeasurementsInstrument.setCurrentIndex(-1)

    def onSearch(self):               
        try:
            conn = QSqlDatabase.database('query')
            query = QSqlQuery(conn)
            queryStr = """
select i.id, m.*
from measurement m, instrument i
where m.instrument_id = i.id and m.measurement_date >= :start_date and m.measurement_date < :end_date
"""
            dtFrom = self.ui.dtMeasurementsFrom.dateTime()
            dtFromStr = dtFrom.toString("yyyy-MM-dd HH:mm:ss")            
            dtTo = self.ui.dtMeasurementsTo.dateTime()
            dtToStr = dtTo.toString("yyyy-MM-dd HH:mm:ss")                                    

            bind_station = False
            if self.ui.cboxMeasurementsStation.currentIndex() > -1:
                stationIndex = self.models.station.index(self.ui.cboxMeasurementsStation.currentIndex(), self.models.station.fieldIndex("id"))
                stationID = self.models.station.data(stationIndex)
                queryStr += " and m.station_id = :station_id"
                bind_station = True                
            
            bind_channels = False
            if self.ui.cboxMeasurementsChannels.currentText():
                channels = int(self.ui.cboxMeasurementsChannels.currentText())
                queryStr += " and i.channel_count = :channel_count"
                bind_channels = True                

            bind_instrument = False
            if self.ui.cboxMeasurementsInstrument.currentIndex() > -1:
                instrumentIndex = self.models.instrument.index(self.ui.cboxMeasurementsInstrument.currentIndex(), self.models.instrument.fieldIndex("id"))
                instrumentID = self.models.instrument.data(instrumentIndex)                        
                queryStr += " and m.instrument_id = :instrument_id"
                bind_instrument = True                
            
            queryStr += " order by m.measurement_date asc"

            query.prepare(queryStr)

            query.bindValue(":start_date", dtFromStr)
            query.bindValue(":end_date", dtToStr)

            if bind_station:
                query.bindValue(":station_id", stationID)

            if bind_channels:
                query.bindValue(":channel_count", channels)

            if bind_instrument:
                query.bindValue(":instrument_id", instrumentID)            
            
            success = query.exec()
            if not success:                                
                UVLog.show_error("Query failed: " + query.lastError().text())
                return 

            self.ui.tblMeasurements.setRowCount(0)                   
            while query.next():
                rowPosition = self.ui.tblMeasurements.rowCount()
                self.ui.tblMeasurements.insertRow(rowPosition)            
                self.ui.tblMeasurements.setItem(rowPosition, 0, QTableWidgetItem(str(query.value("id"))))
                self.ui.tblMeasurements.setItem(rowPosition, 1, QTableWidgetItem(str(query.value("principal"))))
                self.ui.tblMeasurements.setItem(rowPosition, 2, QTableWidgetItem(query.value("measurement_date").toString("yyyy-MM-dd hh:mm:ss")))
                self.ui.tblMeasurements.setItem(rowPosition, 3, QTableWidgetItem(str(query.value("e305"))))
                self.ui.tblMeasurements.setItem(rowPosition, 4, QTableWidgetItem(str(query.value("e313"))))
                self.ui.tblMeasurements.setItem(rowPosition, 5, QTableWidgetItem(str(query.value("e320"))))
                self.ui.tblMeasurements.setItem(rowPosition, 6, QTableWidgetItem(str(query.value("e340"))))
                self.ui.tblMeasurements.setItem(rowPosition, 7, QTableWidgetItem(str(query.value("e380"))))
                self.ui.tblMeasurements.setItem(rowPosition, 8, QTableWidgetItem(str(query.value("e395"))))
                self.ui.tblMeasurements.setItem(rowPosition, 9, QTableWidgetItem(str(query.value("e412"))))
                self.ui.tblMeasurements.setItem(rowPosition, 10, QTableWidgetItem(str(query.value("e443"))))
                self.ui.tblMeasurements.setItem(rowPosition, 11, QTableWidgetItem(str(query.value("e490"))))
                self.ui.tblMeasurements.setItem(rowPosition, 12, QTableWidgetItem(str(query.value("e532"))))
                self.ui.tblMeasurements.setItem(rowPosition, 13, QTableWidgetItem(str(query.value("e555"))))
                self.ui.tblMeasurements.setItem(rowPosition, 14, QTableWidgetItem(str(query.value("e665"))))
                self.ui.tblMeasurements.setItem(rowPosition, 15, QTableWidgetItem(str(query.value("e780"))))
                self.ui.tblMeasurements.setItem(rowPosition, 16, QTableWidgetItem(str(query.value("e875"))))
                self.ui.tblMeasurements.setItem(rowPosition, 17, QTableWidgetItem(str(query.value("e940"))))
                self.ui.tblMeasurements.setItem(rowPosition, 18, QTableWidgetItem(str(query.value("e1020"))))
                self.ui.tblMeasurements.setItem(rowPosition, 19, QTableWidgetItem(str(query.value("e1245"))))
                self.ui.tblMeasurements.setItem(rowPosition, 20, QTableWidgetItem(str(query.value("e1640"))))
                self.ui.tblMeasurements.setItem(rowPosition, 21, QTableWidgetItem(str(query.value("par"))))
                self.ui.tblMeasurements.setItem(rowPosition, 22, QTableWidgetItem(str(query.value("dtemp"))))
                self.ui.tblMeasurements.setItem(rowPosition, 23, QTableWidgetItem(str(query.value("zenith"))))
                self.ui.tblMeasurements.setItem(rowPosition, 24, QTableWidgetItem(str(query.value("azimuth"))))
                
                for i in range(3, 25):
                    self.ui.tblMeasurements.setItemDelegateForColumn(i, self.channelFormat_delegate)
            
            UVLog.show_message("Showing %d measurements" % (self.ui.tblMeasurements.rowCount()))

        except Exception as ex:
            UVLog.show_error(str(ex), True)

    def onEnablePrincipal(self):
        indexes = self.ui.tblMeasurements.selectedIndexes()
        if len(indexes) == 0:
            UVLog.show_error("No rows selected")
            return

        instrumentIndex = self.models.instrument.index(self.ui.cboxMeasurementsInstrument.currentIndex(), self.models.instrument.fieldIndex("id"))
        instrumentID = self.models.instrument.data(instrumentIndex)            
        stationIndex = self.models.station.index(self.ui.cboxMeasurementsStation.currentIndex(), self.models.station.fieldIndex("id"))
        stationID = self.models.station.data(stationIndex) 
        dtFromStr = self.ui.tblMeasurements.item(indexes[0].row(), 1).text()
        dtToStr = self.ui.tblMeasurements.item(indexes[-1].row(), 1).text()        

        conn = QSqlDatabase.database('query')
        conn.transaction()
        query = QSqlQuery(conn)
        query.prepare(
            """
            update measurement 
            set principal = 0 
            where station_id = ? and instrument_id <> ? and measurement_date >= ? and measurement_date <= ? 
            """
        )
        query.addBindValue(stationID)
        query.addBindValue(instrumentID)
        query.addBindValue(dtFromStr)
        query.addBindValue(dtToStr)        
        success = query.exec_()
        if not success:
            conn.rollback()
            UVLog.show_error("Query failed: " + conn.lastError().text())
            return        
        query.prepare(
            """
            update measurement 
            set principal = 1 
            where station_id = ? and instrument_id = ? and measurement_date >= ? and measurement_date <= ? 
            """
        )
        query.addBindValue(stationID)
        query.addBindValue(instrumentID)
        query.addBindValue(dtFromStr)
        query.addBindValue(dtToStr)
        success = query.exec_()
        if not success:
            conn.rollback()
            UVLog.show_error("Query failed: " + conn.lastError().text())
            return        
        conn.commit()         
        self.onSearch()
        UVLog.show_message("Principal enabled from " + dtFromStr + " to " + dtToStr)        

    def onDisablePrincipal(self):
        indexes = self.ui.tblMeasurements.selectedIndexes()
        if len(indexes) == 0:
            UVLog.show_error("No rows selected")
            return

        instrumentIndex = self.models.instrument.index(self.ui.cboxMeasurementsInstrument.currentIndex(), self.models.instrument.fieldIndex("id"))
        instrumentID = self.models.instrument.data(instrumentIndex)
        stationIndex = self.models.station.index(self.ui.cboxMeasurementsStation.currentIndex(), self.models.station.fieldIndex("id"))
        stationID = self.models.station.data(stationIndex) 
        dtFromStr = self.ui.tblMeasurements.item(indexes[0].row(), 1).text()
        dtToStr = self.ui.tblMeasurements.item(indexes[-1].row(), 1).text()        
        
        conn = QSqlDatabase.database('query')
        conn.transaction()
        query = QSqlQuery(conn)        
        query.prepare(
            """
            update measurement 
            set principal = 0 
            where station_id = ? and instrument_id = ? and measurement_date >= ? and measurement_date <= ? 
            """
        )
        query.addBindValue(stationID)
        query.addBindValue(instrumentID)
        query.addBindValue(dtFromStr)
        query.addBindValue(dtToStr)        
        success = query.exec_()
        if not success:
            conn.rollback()
            UVLog.show_error("Query failed: " + conn.lastError().text())
            return                
        conn.commit()        
        self.onSearch()
        UVLog.show_message("Principal disabled from " + dtFromStr + " to " + dtToStr)        

    def onSetStation(self):               
        indexes = self.ui.tblMeasurements.selectedIndexes()
        if len(indexes) == 0:
            UVLog.show_error("No rows selected")
            return
        dlg = UVManStationSelect(self.parent, self.models.station)
        dlg.setWindowModality(Qt.ApplicationModal)
        if dlg.exec_() != QDialog.Accepted:
            return        
        instrumentIndex = self.models.instrument.index(self.ui.cboxMeasurementsInstrument.currentIndex(), self.models.instrument.fieldIndex("id"))
        instrumentID = self.models.instrument.data(instrumentIndex)                    
        conn = QSqlDatabase.database('query')
        conn.transaction()
        query = QSqlQuery(conn)        
        query.prepare(
            """
            update measurement 
            set station_id = :station_id 
            where instrument_id = :instrument_id and measurement_date = :measurement_date
            """
        )
        for index in indexes:
            dt = self.ui.tblMeasurements.item(index.row(), 1).text()
            query.bindValue(":station_id", dlg.selectedStationID)
            query.bindValue(":instrument_id", instrumentID)
            query.bindValue(":measurement_date", dt)
            success = query.exec_()
            if not success:
                conn.rollback()
                UVLog.show_error("Query failed: " + conn.lastError().text())
                return                
        conn.commit()        
        self.onSearch()
        UVLog.show_message("Station changed")   

    def onDelete(self):               
        indexes = self.ui.tblMeasurements.selectedIndexes()
        if len(indexes) == 0:
            UVLog.show_error("No rows selected")
            return
        ret = QMessageBox.question(self.parent, 'Confirmation', "Are you sure you want to delete these measurements?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ret == QMessageBox.No:
            return
        instrumentIndex = self.models.instrument.index(self.ui.cboxMeasurementsInstrument.currentIndex(), self.models.instrument.fieldIndex("id"))
        instrumentID = self.models.instrument.data(instrumentIndex)                    
        stationIndex = self.models.station.index(self.ui.cboxMeasurementsStation.currentIndex(), self.models.station.fieldIndex("id"))
        stationID = self.models.station.data(stationIndex) 
        conn = QSqlDatabase.database('query')
        conn.transaction()
        query = QSqlQuery(conn)        
        query.prepare(
            """
            delete from measurement 
            where station_id = :station_id and instrument_id = :instrument_id and measurement_date = :measurement_date
            """
        )
        for index in indexes:
            dt = self.ui.tblMeasurements.item(index.row(), 1).text()
            query.bindValue(":station_id", stationID)
            query.bindValue(":instrument_id", instrumentID)
            query.bindValue(":measurement_date", dt)
            success = query.exec_()
            if not success:
                conn.rollback()
                UVLog.show_error("Query failed: " + conn.lastError().text())
                return                
        conn.commit()        
        self.onSearch()
        UVLog.show_message("Measurements deleted")   
