# -*- coding: utf-8 -*-

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QDialog
from datetime import datetime
from uvman_uvlog import UVLog

class UVManFactorNew(QDialog):
    def __init__(self, parent, instrument_id, factortype_id):
        super(UVManFactorNew, self).__init__(parent)    

        self.parent = parent
        self.settings = self.parent.settings        
        self.models = parent.models
        self.instrument_id = instrument_id
        self.factortype_id = factortype_id
        self.ui = uic.loadUi('uvman_factor_new.ui', self)

        self.ui.editInstrumentID.setText(str(self.instrument_id))
        self.ui.editFactorID.setText(str(self.factortype_id))
        self.ui.dtValidFrom.setDateTime(datetime.now())
        self.ui.dtValidTo.setDateTime(datetime.now())    

        self.need_refresh = False

    def needRefresh(self):
        return self.need_refresh

    def accept(self):   
        try:     
            instid, factid, validFrom, validTo = 0, 0, datetime.now(), datetime.now()
            e305, e313, e320, e340, e380, e395, e412, e443, e490, e532 = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
            e555, e665, e780, e875, e940, e1020, e1245, e1640, par = 1, 1, 1, 1, 1, 1, 1, 1, 1            

            if not self.ui.editInstrumentID.text():
                UVLog.show_error("Missing ID for instrument")
                return
            instid = self.ui.editInstrumentID.text()

            if not self.ui.editFactorID.text():
                UVLog.show_error("Missing ID for factor type")
                return
            factid = self.ui.editFactorID.text()                    

            validFrom = self.ui.dtValidFrom.dateTime()
            validTo = self.ui.dtValidTo.dateTime()

            if not self.ui.editC305.text():
                UVLog.show_error("Missing c305")
                return
            e305 = self.ui.editC305.text()            

            if not self.ui.editC313.text():
                UVLog.show_error("Missing c313")
                return
            e313 = self.ui.editC313.text()

            if not self.ui.editC320.text():
                UVLog.show_error("Missing c320")
                return
            e320 = self.ui.editC320.text()

            if not self.ui.editC340.text():
                UVLog.show_error("Missing c340")
                return
            e340 = self.ui.editC340.text()

            if not self.ui.editC380.text():
                UVLog.show_error("Missing c380")
                return
            e380 = self.ui.editC380.text()

            if not self.ui.editC395.text():
                UVLog.show_error("Missing c395")
                return
            e395 = self.ui.editC395.text()

            if not self.ui.editC412.text():
                UVLog.show_error("Missing c412")
                return
            e412 = self.ui.editC412.text()

            if not self.ui.editC443.text():
                UVLog.show_error("Missing c443")
                return
            e443 = self.ui.editC443.text()

            if not self.ui.editC490.text():
                UVLog.show_error("Missing c490")
                return
            e490 = self.ui.editC490.text()

            if not self.ui.editC532.text():
                UVLog.show_error("Missing c532")
                return
            e532 = self.ui.editC532.text()

            if not self.ui.editC555.text():
                UVLog.show_error("Missing c555")
                return
            e555 = self.ui.editC555.text()

            if not self.ui.editC665.text():
                UVLog.show_error("Missing c665")
                return
            e665 = self.ui.editC665.text()

            if not self.ui.editC780.text():
                UVLog.show_error("Missing c780")
                return
            e780 = self.ui.editC780.text()

            if not self.ui.editC875.text():
                UVLog.show_error("Missing c875")
                return
            e875 = self.ui.editC875.text()

            if not self.ui.editC940.text():
                UVLog.show_error("Missing c940")
                return
            e940 = self.ui.editC940.text()

            if not self.ui.editC1020.text():
                UVLog.show_error("Missing c1020")
                return
            e1020 = self.ui.editC1020.text()

            if not self.ui.editC1245.text():
                UVLog.show_error("Missing c1245")
                return
            e1245 = self.ui.editC1245.text()

            if not self.ui.editC1640.text():
                UVLog.show_error("Missing c1640")
                return
            e1640 = self.ui.editC1640.text()

            if not self.ui.editPar.text():
                UVLog.show_error("Missing Par")
                return
            par = self.ui.editPar.text()

            mfact = self.models.factor
            row = mfact.rowCount()
            mfact.insertRow(row)
            mfact.setData(mfact.index(row, 1), instid)
            mfact.setData(mfact.index(row, 2), factid)
            mfact.setData(mfact.index(row, 3), validFrom)
            mfact.setData(mfact.index(row, 4), validTo)
            mfact.setData(mfact.index(row, 5), e305)
            mfact.setData(mfact.index(row, 6), e313)
            mfact.setData(mfact.index(row, 7), e320)
            mfact.setData(mfact.index(row, 8), e340)
            mfact.setData(mfact.index(row, 9), e380)
            mfact.setData(mfact.index(row, 10), e395)
            mfact.setData(mfact.index(row, 11), e412)
            mfact.setData(mfact.index(row, 12), e443)
            mfact.setData(mfact.index(row, 13), e490)
            mfact.setData(mfact.index(row, 14), e532)
            mfact.setData(mfact.index(row, 15), e555)
            mfact.setData(mfact.index(row, 16), e665)
            mfact.setData(mfact.index(row, 17), e780)
            mfact.setData(mfact.index(row, 18), e875)
            mfact.setData(mfact.index(row, 19), e940)
            mfact.setData(mfact.index(row, 20), e1020)
            mfact.setData(mfact.index(row, 21), e1245)
            mfact.setData(mfact.index(row, 22), e1640)
            mfact.setData(mfact.index(row, 23), par)            
            if not mfact.submitAll():
                msg = mfact.lastError()
                mfact.revertAll()
                UVLog.show_error("Unable to create factors for %s|%s: %s" % (instid, factid, msg))
                return            
            mfact.select()
            self.need_refresh = True
            self.close()
        except Exception as ex:
            UVLog.show_error(str(ex), True)