# -*- coding: utf-8 -*-

import os, sys

import uvman_log, resources
from pathlib import Path
from PyQt5 import uic
from PyQt5.QtCore import QLocale, QSettings
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtSql import QSqlDatabase
from uvman_models import UVMAN_Models
from uvman_instrument import UVMAN_Instrument
from uvman_station import UVMAN_Station
from uvman_measurement import UVMAN_Measurement
from uvman_factor import UVMAN_Factor
from uvman_product import UVMAN_Product
from uvman_uvlog import UVLog

class UVManagerException(Exception):
    pass

class UVManager(QMainWindow):
    def __init__(self, log):
        super(UVManager, self).__init__()                        
                        
        self.ui = uic.loadUi('uvman.ui', self) 
        UVLog.init(log, self.ui.statusBar)
        UVLog.log_message('Loading GUI')

        script_dir = Path( __file__ ).parent.absolute()
        UVLog.log_message("Using script directory: %s" % script_dir) 

        config_file = script_dir / "config.ini"
        if not config_file.exists():
            raise UVManagerException("No config file found (%s)" % config_file)
        UVLog.log_message("Using config file: %s" % config_file) 
                
        self.settings = QSettings(str(config_file), QSettings.IniFormat)        

    def initialize(self, log):
        
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

        UVLog.log_message('Setup UI components')
        self.uvman_station = UVMAN_Station(self)
        self.uvman_instrument = UVMAN_Instrument(self)
        self.uvman_measurement = UVMAN_Measurement(self)        
        self.uvman_factor = UVMAN_Factor(self)        
        self.uvman_product = UVMAN_Product(self)
        
        self.ui.tabs.currentChanged.connect(self.onTabsCurrentChanged)
        self.ui.tabs.setCurrentIndex(1)        

    def onTabsCurrentChanged(self, index):
        if index == 4:
            self.uvman_factor.onSelectFactor()    

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