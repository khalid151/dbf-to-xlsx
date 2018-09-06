#!/bin/python3
import GUI
import sys
import Resources
from Converter import convert
from PyQt5 import QtWidgets, QtGui, QtCore

class MainWindow(QtWidgets.QMainWindow, GUI.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("DBF to Xlsx")

        icon = [QtGui.QIcon() for _ in range(4)]
        icon[0].addPixmap(QtGui.QPixmap(":/images/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon[1].addPixmap(QtGui.QPixmap(":/images/remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon[2].addPixmap(QtGui.QPixmap(":/images/convert.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon[3].addPixmap(QtGui.QPixmap(":/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_button.setIcon(icon[0])
        self.remove_button.setIcon(icon[1])
        self.convert_button.setIcon(icon[2])
        self.add_button.clicked.connect(self.add_clicked)
        self.remove_button.clicked.connect(self.remove_clicked)
        self.convert_button.clicked.connect(self.convert_clicked)
        self.setWindowIcon(icon[3])

    def create_message(self, text, icon=QtWidgets.QMessageBox.Information):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(icon)
        msg.setText(text)
        msg.setStandardButtons(msg.Ok)
        msg.exec_()

    def add_clicked(self):
        layout = QtWidgets.QHBoxLayout()
        button_1 = QtWidgets.QPushButton('Students')
        button_2 = QtWidgets.QPushButton('Subjects')
        lineEdit = QtWidgets.QLineEdit()
        button_1.setFlat(True)
        button_2.setFlat(True)
        button_1.clicked.connect(self.student_item_clicked)
        button_2.clicked.connect(self.subject_item_clicked)
        lineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        lineEdit.setPlaceholderText("Year")
        layout.addWidget(button_1)
        layout.addWidget(button_2)
        layout.addWidget(lineEdit)
        checkBox = QtWidgets.QCheckBox()
        checkBox.setHidden(True)
        self.items.addRow(checkBox, layout)

    def convert_clicked(self):
        if not self.items.rowCount():
            return
        to_convert = []
        for i in range(self.items.rowCount()):
            layout = self.items.itemAt(i, 1)
            stud = layout.itemAt(0).widget().objectName()
            sub = layout.itemAt(1).widget().objectName()
            year = layout.itemAt(2).widget().text()
            to_convert.append((stud, sub, year))
            if not year:
                self.create_message("Make sure you filled year field.")
                to_convert = []
                return
        saving_dir = QtWidgets.QFileDialog.getExistingDirectory()
        if not saving_dir:
            self.create_message("Select a saving folder.")
            return
        for files in to_convert:
            output = f"{saving_dir}/{files[2]}.xlsx"
            convert(files[0], files[1], output)
            self.create_message("Done!", 0)

    def remove_clicked(self):
        if 'Remove' in self.sender().text() and self.items.rowCount() > 0:
            for i in range(self.items.rowCount()):
                self.items.itemAt(i, 0).widget().setHidden(False)
            self.sender().setText('Confirm')
        elif 'Confirm' in self.sender().text().replace('&', ''):
            msg = QtWidgets.QMessageBox()
            msg.setText("Are you sure?")
            msg.setStandardButtons(msg.Yes | msg.No)
            if msg.exec_() == msg.Yes:
                def clear(items):
                    for i in range(items.rowCount()):
                        try:
                            cb = items.itemAt(i, 0).widget()
                            if cb.checkState():
                                items.removeRow(i)
                                clear(items)
                        except AttributeError:
                            break
                clear(self.items)
            for i in range(self.items.rowCount()):
                check_box = self.items.itemAt(i, 0).widget()
                check_box.setHidden(True)
                check_box.setCheckState(False)
            self.sender().setText('Remove')

    def student_item_clicked(self):
        stud_file = QtWidgets.QFileDialog.getOpenFileName(filter="*.dbf")[0]
        stud = stud_file.split('/')[-1]
        self.sender().setText(stud)
        self.sender().setObjectName(stud_file)

    def subject_item_clicked(self):
        sub_file = QtWidgets.QFileDialog.getOpenFileName(filter="*.dbf")[0]
        sub = sub_file.split('/')[-1]
        self.sender().setText(sub)
        self.sender().setObjectName(sub_file)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_form = MainWindow()
    main_form.show()
    app.exec_()

if __name__ == '__main__':
    sys.exit(main())
