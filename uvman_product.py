# -*- coding: utf-8 -*-

from uvman_uvlog import UVLog
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from uvman_product_new import UVManProductNew
from uvman_product_edit import UVManProductEdit

class UVMAN_Product():
    def __init__(self, parent):
        self.parent = parent
        self.settings = self.parent.settings        
        self.ui = self.parent.ui         
        self.models = self.parent.models

        self.ui.tblProducts.setModel(self.models.product)         
        header = self.ui.tblProducts.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)       
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignLeft)        

        self.ui.btnProductsNew.clicked.connect(self.onNew)
        self.ui.btnProductsEdit.clicked.connect(self.onEdit)
        self.ui.btnProductsDelete.clicked.connect(self.onDelete)

    def onNew(self):
        dlg = UVManProductNew(self, self.models.product)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()        

    def onEdit(self):
        index = self.ui.tblProducts.currentIndex()
        if not index.isValid():            
            UVLog.show_error("No row selected")
            return
        dlg = UVManProductEdit(self, index, self.models.product)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()        

    def onDelete(self):
        index = self.ui.tblProducts.currentIndex()
        if not index.isValid():        
            UVLog.show_error("No row selected")
            return
        record = self.models.product.record(index.row())
        name = record.value(1)        
        if (QMessageBox.question(self.parent, "Confirmation", ("Delete {0} from models?".format(name)), QMessageBox.Yes | QMessageBox.No) == QMessageBox.No):
            return
        self.models.product.removeRow(index.row())
        if not self.models.product.submitAll():
            self.models.product.revertAll()            
            UVLog.show_error("Unable to remove product " + name)        
            return
        self.models.product.select()
        UVLog.show_message("Product " + name + " deleted")    