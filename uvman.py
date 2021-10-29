import os, sys

from PyQt5 import QtWidgets
import uvman_log, resources
from pathlib import Path
from PyQt5 import uic
from PyQt5.QtCore import QLocale, QSettings, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMessageBox, qApp, QAbstractItemView
from PyQt5.QtSql import QSqlDatabase
from uvman_station_new import UVManStationNew
from uvman_station_edit import UVManStationEdit
from uvman_instrument_new import UVManInstrumentNew
from uvman_instrument_edit import UVManInstrumentEdit
from uvman_delegates import PasswordDelegate
from uvman_models import UVMAN_Models
from uvman_measurements import UVMAN_Measurements
from uvman_uvlog import UVLog

class UVManagerException(Exception):
    pass

class UVManager(QMainWindow):
    def __init__(self, log):
        super(UVManager, self).__init__()                        
                        
        self.ui = uic.loadUi('uvman.ui', self) 
        UVLog.init(log, self.ui.statusBar)
        UVLog.log_message('Loading GUI')

        config_dir = os.path.expandvars(r'%PUBLIC%\uvnet')
        os.makedirs(config_dir, exist_ok = True)
        settings_file = "uvman.ini"
        settings_path = Path(config_dir) / settings_file
        self.settings = QSettings(str(settings_path), QSettings.IniFormat)

        UVLog.log_message("Settings file: " + str(settings_path))                  

    def initialize(self, log):

        self.password_delegate = PasswordDelegate()        

        UVLog.log_message('Creating menus')

        menuFile = self.ui.menuBar.addMenu('&File')
        actionExit = QAction('E&xit', self)
        actionExit.setShortcut('Ctrl+Q')
        actionExit.setStatusTip('Exit application')
        actionExit.triggered.connect(self.quit)
        menuFile.addAction(actionExit)        

        UVLog.log_message('Open database')
        
        connection_string = None
        if self.settings.contains("connection_string"):                        
            connection_string = self.settings.value('connection_string')        
        else:            
            connection_string = 'Driver={SQL Server};Server=localhost,1433;Database=UVNET2;Uid=uvnet_user;Pwd=uvnet_password;'
            self.settings.setValue('connection_string', connection_string)            

        conn_model = QSqlDatabase.addDatabase('QODBC', 'model')        
        conn_model.setDatabaseName(self.settings.value('connection_string'))
        if not conn_model.open():
            UVLog.show_message(conn_model.lastError().text())
            return

        conn_query = QSqlDatabase.addDatabase('QODBC', 'query')        
        conn_query.setDatabaseName(self.settings.value('connection_string'))
        if not conn_query.open():
            UVLog.show_message(conn_query.lastError().text())
            return

        UVLog.log_message('Creating models')
        self.models = UVMAN_Models(self, log)        

        self.ui.tblStations.setModel(self.models.station)
        self.ui.tblStations.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.ui.tblStations.setStyleSheet("QHeaderView::section { background-color: rgba(0, 0, 255, 128) }")
        self.ui.tblStations.setItemDelegateForColumn(7, self.password_delegate)        
        header = self.ui.tblStations.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)       
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignLeft)

        self.ui.cboxMeasurementsStation.setModel(self.models.station)
        vcMeasurementsStation = self.models.station.fieldIndex('label')
        self.ui.cboxMeasurementsStation.setModelColumn(vcMeasurementsStation)        

        self.ui.tblInstruments.setModel(self.models.instrument)
        self.ui.tblInstruments.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.ui.tblInstruments.setItemDelegate(QSqlRelationalDelegate(self.ui.tblInstruments))        
        header = self.ui.tblInstruments.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)       
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignLeft)

        self.ui.cboxMeasurementsInstrument.setModel(self.models.instrument)
        vcMeasurementsInstrument = self.models.instrument.fieldIndex('id')
        self.ui.cboxMeasurementsInstrument.setModelColumn(vcMeasurementsInstrument)        

        self.ui.tblProducts.setModel(self.models.product)         
        header = self.ui.tblProducts.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)       
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignLeft)

        self.ui.cboxFactorsProducts.setModel(self.models.product)
        viewColumn = self.models.product.fieldIndex('label')
        self.ui.cboxFactorsProducts.setModelColumn(viewColumn)
        
        header = self.ui.tblMeasurements.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)       
        #header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignLeft)

        # Connect signals
        UVLog.log_message('Connecting signals')
        
        self.ui.btnStationNew.clicked.connect(self.onNewStation)
        self.ui.btnStationEdit.clicked.connect(self.onEditStation)
        self.ui.btnStationDelete.clicked.connect(self.onDeleteStation)
        self.ui.btnInstrumentNew.clicked.connect(self.onNewInstrument)
        self.ui.btnInstrumentEdit.clicked.connect(self.onEditInstrument)
        self.ui.btnInstrumentDelete.clicked.connect(self.onDeleteInstrument)  

        self.uvman_measurements = UVMAN_Measurements(self)
        self.ui.btnMeasurementsSearch.clicked.connect(self.uvman_measurements.onMeasurementsSearch)      
        self.ui.btnMeasurementsEnablePrincipal.clicked.connect(self.uvman_measurements.onEnablePrincipal)      
        self.ui.btnMeasurementsDisablePrincipal.clicked.connect(self.uvman_measurements.onDisablePrincipal)      
        self.ui.btnMeasurementsSetStation.clicked.connect(self.uvman_measurements.onSetStation)      
        self.ui.btnMeasurementsDelete.clicked.connect(self.uvman_measurements.onDelete)         

    def onNewStation(self):    
        dlg = UVManStationNew(self, self.models.station)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()        

    def onEditStation(self):    
        index = self.ui.tblStations.currentIndex()
        if not index.isValid():        
            UVLog.show_error("No row selected")
            return
        dlg = UVManStationEdit(self, index, self.models.station)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()        

    def onDeleteStation(self):               
        index = self.ui.tblStations.currentIndex()
        if not index.isValid():        
            UVLog.show_error("No row selected")
            return
        record = self.models.station.record(index.row())
        name = record.value(1)        
        if (QMessageBox.question(self, "Confirmation", ("Delete {0} from stations?".format(name)), QMessageBox.Yes | QMessageBox.No) == QMessageBox.No):
            return
        self.models.station.removeRow(index.row())
        if not self.models.station.submitAll():
            self.models.station.revertAll()            
            UVLog.show_error("Unable to remove station " + name)        
            return
        self.models.station.select()
        UVLog.show_message("Station " + name + " deleted")    

    def onNewInstrument(self):    
        dlg = UVManInstrumentNew(self, self.models.instrument, self.models.station)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()        

    def onEditInstrument(self):    
        index = self.ui.tblInstruments.currentIndex()
        if not index.isValid():            
            UVLog.show_error("No row selected")
            return
        dlg = UVManInstrumentEdit(self, index, self.models.instrument, self.models.station)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()        

    def onDeleteInstrument(self):               
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

    def quit(self):
        qApp.quit()    

if __name__ == '__main__':
    try:        
        log = uvman_log.create_log("uvman")           
        log.info("=========== START UVMAN ===========")         

        app = QApplication(sys.argv)  

        QLocale.setDefault(QLocale(QLocale.C))
              
        app_icon = QIcon()
        app_icon.addFile(":/images/uvman-16.png")
        app_icon.addFile(":/images/uvman-24.png")
        app_icon.addFile(":/images/uvman-32.png")
        app_icon.addFile(":/images/uvman-48.png")
        app_icon.addFile(":/images/uvman-64.png")
        app_icon.addFile(":/images/uvman-128.png")
        app_icon.addFile(":/images/uvman-256.png")
        app_icon.addFile(":/images/uvman-512.png")
        app.setWindowIcon(app_icon) 
        
        font = QApplication.font()
        font.setPointSize(10)
        QApplication.setFont(font)

        uvm = UVManager(log)        
        uvm.setWindowIcon(app_icon)
        uvm.initialize(log)
        uvm.show()

        app.exec_()
        log.info('Exiting uvman')
    except UVManagerException as uvmex:
        log.error(str(uvmex))
    except Exception as ex:
        print(str(ex))