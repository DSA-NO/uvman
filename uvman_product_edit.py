from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from uvman_uvlog import UVLog

class UVManProductEdit(QDialog):
    def __init__(self, parent, index):
        super(UVManProductEdit, self).__init__(parent)    

        self.parent = parent
        self.settings = self.parent.settings
        self.models = self.parent.models        
        self.index = index        

        self.ui = uic.loadUi('uvman_product_edit.ui', self)         

        record = self.models.product.record(self.index.row())
        self.ui.tbName.setText(record.value(1))        

    def accept(self):   
        try:                 
            if not self.ui.tbName.text():
                UVLog.show_error("Missing name for product")
                return

            name = self.ui.tbName.text()            

            UVLog.show_message("Renaming product to " + name)    

            mprod = self.models.product
            row = self.index.row()            
            mprod.setData(mprod.index(row, 1), name)            
            if not mprod.submitAll():
                mprod.revertAll()
                UVLog.show_error("Unable to update product " + name)
                return
            mprod.select()
            self.close() 
        except Exception as ex:
            UVLog.show_error(str(ex), True)
