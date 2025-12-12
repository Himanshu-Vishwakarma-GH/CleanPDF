from PyQt6.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    finished = pyqtSignal(bool, str) # success, message
    
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        try:
            # Execute the function
            result = self.func(*self.args, **self.kwargs)
            # Result is expected to be (bool, str) from our Ops modules
            if isinstance(result, tuple) and len(result) == 2:
                success, msg = result
                self.finished.emit(success, msg)
            else:
                self.finished.emit(True, "Operation completed (No standard return detected)")
        except Exception as e:
            self.finished.emit(False, str(e))
