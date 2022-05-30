from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from uvman_uvlog import UVLog

class UVManProductEdit(QDialog):
    def __init__(self, parent, index, model):
        super(UVManProductEdit, self).__init__(parent)    

        self.ui = uic.loadUi('uvman_product_edit.ui', self) 
        self.settings = parent.settings
        self.index = index
        self.model = model
        record = self.model.record(self.index.row())
        self.ui.tbName.setText(record.value(1))        

    def accept(self):   
        try:                 
            if not self.ui.tbName.text():
                UVLog.show_error("Missing name for product")
                return

            name = self.ui.tbName.text()            

            UVLog.show_message("Renaming product to " + name)    

            row = self.index.row()            
            self.model.setData(self.model.index(row, 1), name)            
            if not self.model.submitAll():
                self.model.revertAll()
                UVLog.show_error("Unable to update product " + name)
                return
            self.model.select()
            self.close() 
        except Exception as ex:
            UVLog.show_error(str(ex), True)
