from PyQt5.QtCore import QThread

from scan_hostnames import runner


class Worker(QThread):
    def __init__(self, parent=None):
        super().__init__()
        self._parent = parent

    def run(self):
        while True:
            runner(self._parent)
            self.sleep(60)
