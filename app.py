import sys

from PyQt5 import QtWidgets

from ui import Window

app = QtWidgets.QApplication(sys.argv)
ui = Window()
ui.show()
ui.actionExit.triggered.connect(app.quit)
ui.actionSave.triggered.connect(ui.save)
ui.actionReload.triggered.connect(ui.reload)
ui.reload()
sys.exit(app.exec_())
