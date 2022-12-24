import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon

from workerThread import Worker


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_icon = QIcon('assets/list.png')
        self.logout_icon = QIcon("assets/logout.png")
        self.save_icon = QIcon("assets/save.png")
        self.reload_icon = QIcon("assets/refresh.png")

        self.setObjectName("self")
        self.resize(400, 670)
        self.setWindowIcon(self.main_icon)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hostnameList = QtWidgets.QListWidget(self.centralwidget)
        self.hostnameList.setObjectName("hostnameList")
        self.horizontalLayout.addWidget(self.hostnameList)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 339, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(self)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setIcon(self.save_icon)
        self.action = QtWidgets.QAction(self)
        self.action.setObjectName("action")
        self.actionExit = QtWidgets.QAction(self)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.setIcon(self.logout_icon)
        self.actionReload = QtWidgets.QAction(self)
        self.actionReload.setObjectName("actionReload")
        self.actionReload.setIcon(self.reload_icon)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionReload)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.thread = Worker(self)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "NetList"))
        self.menuFile.setTitle(_translate("self", "File"))
        self.actionSave.setText(_translate("self", "Save"))
        self.action.setText(_translate("self", "___________________________"))
        self.actionExit.setText(_translate("self", "Exit"))
        self.actionReload.setText(_translate("self", "Reload"))

    def save(self):
        with open(f'{time.time()}.hostnames.lst', 'w') as file:
            for i in range(self.hostnameList.count()):
                file.write(self.hostnameList.item(i).text() + "\n")

    def closeEvent(self, event):
        self.thread.exit(0)
        self.close()

    def reload(self):
        self.thread.start()
        self.hostnameList.clear()
