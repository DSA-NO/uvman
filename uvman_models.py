from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlRelation, QSqlRelationalTableModel, QSqlTableModel

class UVMAN_Models():
    def __init__(self, parent, log):            
        conn = QSqlDatabase.database('model')
        
        # Station model
        self.station = QSqlTableModel(parent, conn)
        self.station.setEditStrategy(QSqlTableModel.OnManualSubmit)        
        self.station.setTable('station')        
        self.station.setSort(1, Qt.AscendingOrder)
        self.station.select()
        self.station.setHeaderData(0, Qt.Horizontal, "ID")
        self.station.setHeaderData(1, Qt.Horizontal, "Name")
        self.station.setHeaderData(2, Qt.Horizontal, "Active")
        self.station.setHeaderData(3, Qt.Horizontal, "Latitude")
        self.station.setHeaderData(4, Qt.Horizontal, "Longitude")
        self.station.setHeaderData(5, Qt.Horizontal, "FTP Host")
        self.station.setHeaderData(6, Qt.Horizontal, "FTP User")
        self.station.setHeaderData(7, Qt.Horizontal, "FTP Password")
        self.station.setHeaderData(8, Qt.Horizontal, "FTP Remote Dir")
        self.station.setHeaderData(9, Qt.Horizontal, "FTP Local Dir")        
        self.station.setHeaderData(10, Qt.Horizontal, "Comment")    
        self.station.setHeaderData(11, Qt.Horizontal, "FTP Passive Mode")

        # Instrument model
        self.instrument = QSqlRelationalTableModel(parent, conn)
        self.instrument.setEditStrategy(QSqlTableModel.OnManualSubmit)        
        self.instrument.setTable('instrument') 
        self.instrument.setSort(0, Qt.AscendingOrder)
        self.instrument.setRelation(2, QSqlRelation("station", "id", "label"));       
        self.instrument.select()        
        self.instrument.setHeaderData(0, Qt.Horizontal, "ID")
        self.instrument.setHeaderData(1, Qt.Horizontal, "Name")
        self.instrument.setHeaderData(2, Qt.Horizontal, "Station")
        self.instrument.setHeaderData(3, Qt.Horizontal, "Active")
        self.instrument.setHeaderData(4, Qt.Horizontal, "Principal")
        self.instrument.setHeaderData(5, Qt.Horizontal, "Model")
        self.instrument.setHeaderData(6, Qt.Horizontal, "Chan. Count")
        self.instrument.setHeaderData(7, Qt.Horizontal, "Last Calib.")
        self.instrument.setHeaderData(8, Qt.Horizontal, "Fetch Mod.")
        self.instrument.setHeaderData(9, Qt.Horizontal, "Validate Mod.")
        self.instrument.setHeaderData(10, Qt.Horizontal, "Store Mod.")
        self.instrument.setHeaderData(11, Qt.Horizontal, "Match Expression")        
        self.instrument.setHeaderData(12, Qt.Horizontal, "Comment")   

        # Product model
        self.product = QSqlTableModel(parent, conn)
        self.product.setTable('factortype')
        self.product.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.product.select()
        self.product.setHeaderData(0, Qt.Horizontal, "ID")
        self.product.setHeaderData(1, Qt.Horizontal, "Name")         