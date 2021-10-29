from PyQt5.QtCore import QDateTime, QTimer

class UVLog:    
    status = None
    defaultStyle = None
    timer = None 
    log = None   

    @staticmethod    
    def init(log, status):
        UVLog.log = log
        UVLog.status = status
        UVLog.defaultStyle = status.styleSheet()

    @staticmethod    
    def log_message(msg):
        UVLog.log.info(msg)

    @staticmethod    
    def show_message(msg):
        UVLog.log.info(msg)
        if UVLog.timer:
            UVLog.timer.stop()
            UVLog.timer.deleteLater()
        UVLog.timer = QTimer()        
        UVLog.timer.timeout.connect(UVLog.timeout)
        UVLog.timer.setSingleShot(True)
        UVLog.timer.start(5000)
        UVLog.status.setStyleSheet(UVLog.defaultStyle)
        dt = QDateTime.currentDateTime()
        UVLog.status.showMessage(dt.toString("yyyy-MM-dd hh:mm:ss") + " - " + msg)

    @staticmethod    
    def log_error(msg, show_exc=False):
        if show_exc:
            UVLog.log.error(msg, exc_info=True)
        else: 
            UVLog.log.error(msg)

    @staticmethod    
    def show_error(msg, show_exc=False):
        if show_exc:
            UVLog.log.error(msg, exc_info=True)
        else: 
            UVLog.log.error(msg)
        if UVLog.timer:
            UVLog.timer.stop()
            UVLog.timer.deleteLater()
        UVLog.timer = QTimer()
        UVLog.timer.timeout.connect(UVLog.timeout)
        UVLog.timer.setSingleShot(True)
        UVLog.timer.start(10000)
        UVLog.status.setStyleSheet("background-color : Orange")
        dt = QDateTime.currentDateTime()
        UVLog.status.showMessage(dt.toString("yyyy-MM-dd hh:mm:ss") + " - " + msg)

    @staticmethod    
    def timeout():
        UVLog.status.setStyleSheet(UVLog.defaultStyle)
        UVLog.status.showMessage("")