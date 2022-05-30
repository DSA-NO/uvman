from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from uvman_uvlog import UVLog

class UVManProductNew(QDialog):
    def __init__(self, parent):
        super(UVManProductNew, self).__init__(parent)    

        self.parent = parent
        self.settings = self.parent.settings
        self.models = parent.models

        self.ui = uic.loadUi('uvman_product_new.ui', self)         

    def accept(self):   
        try:                 
            if not self.ui.tbName.text():
                UVLog.show_error("Missing name for new product")
                return

            name = self.ui.tbName.text()            

            UVLog.show_message("Creating new product " + name)    

            mprod = self.models.product
            row = mprod.rowCount()
            mprod.insertRow(row)
            mprod.setData(mprod.index(row, 1), name)            
            if not mprod.submitAll():
                mprod.revertAll()
                UVLog.show_error("Unable to create product " + name)
                return
            mprod.select()
            self.close() 
        except Exception as ex:
            UVLog.show_error(str(ex), True)
