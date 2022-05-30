from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from uvman_uvlog import UVLog

class UVManProductNew(QDialog):
    def __init__(self, parent, model):
        super(UVManProductNew, self).__init__(parent.parent)    

        self.ui = uic.loadUi('uvman_product_new.ui', self) 
        self.settings = parent.settings
        self.model = model

    def accept(self):   
        try:                 
            if not self.ui.tbName.text():
                UVLog.show_error("Missing name for new product")
                return

            name = self.ui.tbName.text()            

            UVLog.show_message("Creating new product " + name)    

            row = self.model.rowCount()
            self.model.insertRow(row)
            self.model.setData(self.model.index(row, 1), name)            
            if not self.model.submitAll():
                self.model.revertAll()
                UVLog.show_error("Unable to create product " + name)
                return
            self.model.select()
            self.close() 
        except Exception as ex:
            UVLog.show_error(str(ex), True)
