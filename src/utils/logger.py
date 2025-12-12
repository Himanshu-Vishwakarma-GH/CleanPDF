from PyQt6.QtCore import QObject, pyqtSignal

class Signaller(QObject):
    log_signal = pyqtSignal(str)

class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.signaller = Signaller()
        return cls._instance

    def log(self, message):
        print(message) # Console fallback
        self.signaller.log_signal.emit(message)

logger = Logger()
