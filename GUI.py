# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 450)
        MainWindow.setMinimumSize(QtCore.QSize(450, 450))
        MainWindow.setMaximumSize(QtCore.QSize(450, 450))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.main_buttons = QtWidgets.QHBoxLayout()
        self.main_buttons.setObjectName("main_buttons")
        self.add_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_button.setObjectName("add_button")
        self.main_buttons.addWidget(self.add_button)
        self.remove_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_button.setObjectName("remove_button")
        self.main_buttons.addWidget(self.remove_button)
        self.convert_button = QtWidgets.QPushButton(self.centralwidget)
        self.convert_button.setObjectName("convert_button")
        self.main_buttons.addWidget(self.convert_button)
        self.verticalLayout.addLayout(self.main_buttons)
        self.scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_widget_contents = QtWidgets.QWidget()
        self.scroll_widget_contents.setGeometry(QtCore.QRect(0, 0, 434, 339))
        self.scroll_widget_contents.setObjectName("scroll_widget_contents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scroll_widget_contents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.items = QtWidgets.QFormLayout()
        self.items.setObjectName("items")
        self.verticalLayout_2.addLayout(self.items)
        self.scroll_area.setWidget(self.scroll_widget_contents)
        self.verticalLayout.addWidget(self.scroll_area)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 450, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.add_button.setText(_translate("MainWindow", "Add"))
        self.remove_button.setText(_translate("MainWindow", "Remove"))
        self.convert_button.setText(_translate("MainWindow", "Convert"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

