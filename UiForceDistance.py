# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiForceDistance.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ForceDistance(object):
    def setupUi(self, ForceDistance):
        ForceDistance.setObjectName("ForceDistance")
        ForceDistance.resize(900, 800)
        ForceDistance.setMinimumSize(QtCore.QSize(0, 0))
        ForceDistance.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(ForceDistance)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout1 = QtWidgets.QVBoxLayout()
        self.verticalLayout1.setObjectName("verticalLayout1")
        self.gridLayout1 = QtWidgets.QGridLayout()
        self.gridLayout1.setObjectName("gridLayout1")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setObjectName("label1")
        self.gridLayout1.addWidget(self.label1, 0, 0, 1, 1)
        self.comboBox1 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox1.setObjectName("comboBox1")
        self.gridLayout1.addWidget(self.comboBox1, 1, 0, 1, 1)
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setObjectName("label2")
        self.gridLayout1.addWidget(self.label2, 0, 1, 1, 1)
        self.comboBox2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox2.setObjectName("comboBox2")
        self.gridLayout1.addWidget(self.comboBox2, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout1.addWidget(self.label, 2, 0, 1, 1)
        self.lineEdit2 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit2.sizePolicy().hasHeightForWidth())
        self.lineEdit2.setSizePolicy(sizePolicy)
        self.lineEdit2.setObjectName("lineEdit2")
        self.gridLayout1.addWidget(self.lineEdit2, 2, 1, 1, 1)
        self.verticalLayout1.addLayout(self.gridLayout1)
        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton1.sizePolicy().hasHeightForWidth())
        self.pushButton1.setSizePolicy(sizePolicy)
        self.pushButton1.setObjectName("pushButton1")
        self.verticalLayout1.addWidget(self.pushButton1)
        self.gridLayout2 = QtWidgets.QGridLayout()
        self.gridLayout2.setObjectName("gridLayout2")
        self.lineEdit1 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit1.sizePolicy().hasHeightForWidth())
        self.lineEdit1.setSizePolicy(sizePolicy)
        self.lineEdit1.setObjectName("lineEdit1")
        self.gridLayout2.addWidget(self.lineEdit1, 0, 1, 1, 1)
        self.pushButton3 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton3.sizePolicy().hasHeightForWidth())
        self.pushButton3.setSizePolicy(sizePolicy)
        self.pushButton3.setObjectName("pushButton3")
        self.gridLayout2.addWidget(self.pushButton3, 2, 1, 1, 1)
        self.label3 = QtWidgets.QLabel(self.centralwidget)
        self.label3.setAlignment(QtCore.Qt.AlignCenter)
        self.label3.setObjectName("label3")
        self.gridLayout2.addWidget(self.label3, 0, 0, 1, 1)
        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setObjectName("pushButton2")
        self.gridLayout2.addWidget(self.pushButton2, 2, 0, 1, 1)
        self.verticalLayout1.addLayout(self.gridLayout2)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout1.addWidget(self.listWidget)
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2.setObjectName("horizontalLayout2")
        self.pushButton4 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton4.sizePolicy().hasHeightForWidth())
        self.pushButton4.setSizePolicy(sizePolicy)
        self.pushButton4.setObjectName("pushButton4")
        self.horizontalLayout2.addWidget(self.pushButton4)
        self.pushButton5 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton5.sizePolicy().hasHeightForWidth())
        self.pushButton5.setSizePolicy(sizePolicy)
        self.pushButton5.setObjectName("pushButton5")
        self.horizontalLayout2.addWidget(self.pushButton5)
        self.verticalLayout1.addLayout(self.horizontalLayout2)
        self.pushButton6 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton6.sizePolicy().hasHeightForWidth())
        self.pushButton6.setSizePolicy(sizePolicy)
        self.pushButton6.setObjectName("pushButton6")
        self.verticalLayout1.addWidget(self.pushButton6)
        self.horizontalLayout.addLayout(self.verticalLayout1)
        self.verticalLayout2 = QtWidgets.QVBoxLayout()
        self.verticalLayout2.setObjectName("verticalLayout2")
        self.horizontalLayout.addLayout(self.verticalLayout2)
        ForceDistance.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ForceDistance)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 26))
        self.menubar.setObjectName("menubar")
        ForceDistance.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ForceDistance)
        self.statusbar.setObjectName("statusbar")
        ForceDistance.setStatusBar(self.statusbar)

        self.retranslateUi(ForceDistance)
        QtCore.QMetaObject.connectSlotsByName(ForceDistance)

    def retranslateUi(self, ForceDistance):
        _translate = QtCore.QCoreApplication.translate
        ForceDistance.setWindowTitle(_translate("ForceDistance", "MainWindow"))
        self.label1.setText(_translate("ForceDistance", "AVAILABLE PORTS:"))
        self.label2.setText(_translate("ForceDistance", "SELECT BAUD:"))
        self.label.setText(_translate("ForceDistance", "SELECT RANGE-FREE RANGE"))
        self.pushButton1.setText(_translate("ForceDistance", "CONNECT"))
        self.pushButton3.setText(_translate("ForceDistance", "SAVE MEASUREMENT"))
        self.label3.setText(_translate("ForceDistance", "SELECT DISTANCE"))
        self.pushButton2.setText(_translate("ForceDistance", "MEASURE"))
        self.pushButton4.setText(_translate("ForceDistance", "PLOT"))
        self.pushButton5.setText(_translate("ForceDistance", "SAVE PLOT"))
        self.pushButton6.setText(_translate("ForceDistance", "RESET"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ForceDistance = QtWidgets.QMainWindow()
    ui = Ui_ForceDistance()
    ui.setupUi(ForceDistance)
    ForceDistance.show()
    sys.exit(app.exec_())
