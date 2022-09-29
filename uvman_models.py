from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlRelation, QSqlRelationalTableModel, QSqlTableModel, QSqlQueryModel

class UVMAN_Models():
    def __init__(self, parent):            
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

        # Factor model
        self.factor = QSqlRelationalTableModel(parent, conn)
        self.factor.setEditStrategy(QSqlTableModel.OnManualSubmit)        
        self.factor.setTable('guvfactor') 
        self.factor.setSort(0, Qt.AscendingOrder)
        self.factor.setRelation(1, QSqlRelation("instrument", "id", "label"));
        self.factor.setRelation(2, QSqlRelation("factortype", "id", "label"));
        self.factor.select()        
        self.factor.setHeaderData(0, Qt.Horizontal, "ID")
        self.factor.setHeaderData(1, Qt.Horizontal, "InstrumentID")
        self.factor.setHeaderData(2, Qt.Horizontal, "FactorTypeID")
        self.factor.setHeaderData(3, Qt.Horizontal, "ValidFrom")
        self.factor.setHeaderData(4, Qt.Horizontal, "ValidTo")
        self.factor.setHeaderData(5, Qt.Horizontal, "c305")
        self.factor.setHeaderData(6, Qt.Horizontal, "c313")
        self.factor.setHeaderData(7, Qt.Horizontal, "c320")
        self.factor.setHeaderData(8, Qt.Horizontal, "c340")
        self.factor.setHeaderData(9, Qt.Horizontal, "c380")
        self.factor.setHeaderData(10, Qt.Horizontal, "c395")
        self.factor.setHeaderData(11, Qt.Horizontal, "c412")
        self.factor.setHeaderData(12, Qt.Horizontal, "c443")        
        self.factor.setHeaderData(13, Qt.Horizontal, "c490")   
        self.factor.setHeaderData(14, Qt.Horizontal, "c532")   
        self.factor.setHeaderData(15, Qt.Horizontal, "c555")   
        self.factor.setHeaderData(16, Qt.Horizontal, "c665")   
        self.factor.setHeaderData(17, Qt.Horizontal, "c780")   
        self.factor.setHeaderData(18, Qt.Horizontal, "c875")   
        self.factor.setHeaderData(19, Qt.Horizontal, "c940")   
        self.factor.setHeaderData(20, Qt.Horizontal, "c1020")   
        self.factor.setHeaderData(21, Qt.Horizontal, "c1245")   
        self.factor.setHeaderData(22, Qt.Horizontal, "c1640")   
        self.factor.setHeaderData(23, Qt.Horizontal, "par")   

        # Product model
        self.product = QSqlTableModel(parent, conn)
        self.product.setTable('factortype')
        self.product.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.product.select()
        self.product.setHeaderData(0, Qt.Horizontal, "ID")
        self.product.setHeaderData(1, Qt.Horizontal, "Name")    

        # Channel count model
        self.channel_count = QSqlQueryModel(parent)
        self.channel_count.setQuery("select distinct channel_count from instrument order by channel_count desc", conn);        
        self.channel_count.setHeaderData(0, Qt.Horizontal, "Channels");     