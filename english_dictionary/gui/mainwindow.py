# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setMinimumSize(QtCore.QSize(800, 600))
        self.central_widget.setObjectName("central_widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.central_widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.left_frame = QtWidgets.QFrame(self.central_widget)
        self.left_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.left_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.left_frame.setObjectName("left_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.left_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_4 = QtWidgets.QFrame(self.left_frame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.search_bar = QtWidgets.QLineEdit(self.frame_4)
        self.search_bar.setMaxLength(64)
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.setObjectName("search_bar")
        self.horizontalLayout_3.addWidget(self.search_bar)
        self.search_button = QtWidgets.QPushButton(self.frame_4)
        self.search_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("svgs/search.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.search_button.setIcon(icon)
        self.search_button.setObjectName("search_button")
        self.horizontalLayout_3.addWidget(self.search_button)
        self.add_button = QtWidgets.QPushButton(self.frame_4)
        self.add_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap("svgs/plus.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.add_button.setIcon(icon1)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout_3.addWidget(self.add_button)
        self.verticalLayout.addWidget(self.frame_4)
        self.scrollArea = QtWidgets.QScrollArea(self.left_frame)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 241, 511))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.list_widget = QtWidgets.QListWidget(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_widget.sizePolicy().hasHeightForWidth())
        self.list_widget.setSizePolicy(sizePolicy)
        self.list_widget.setObjectName("list_widget")
        self.verticalLayout_3.addWidget(self.list_widget)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.scrollArea)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 10)
        self.horizontalLayout_2.addWidget(self.left_frame)
        self.right_frame = QtWidgets.QFrame(self.central_widget)
        self.right_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.right_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.right_frame.setObjectName("right_frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.right_frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_5 = QtWidgets.QFrame(self.right_frame)
        self.frame_5.setEnabled(True)
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.edit_button = QtWidgets.QPushButton(self.frame_5)
        self.edit_button.setObjectName("edit_button")
        self.horizontalLayout_4.addWidget(self.edit_button)
        self.delete_button = QtWidgets.QPushButton(self.frame_5)
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout_4.addWidget(self.delete_button)
        self.verticalLayout_2.addWidget(self.frame_5, 0, QtCore.Qt.AlignRight)
        self.text_browser = QtWidgets.QTextBrowser(self.right_frame)
        self.text_browser.setObjectName("text_browser")
        self.verticalLayout_2.addWidget(self.text_browser)
        self.horizontalLayout_2.addWidget(self.right_frame)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)
        MainWindow.setCentralWidget(self.central_widget)

        self.retranslateUi(MainWindow)
        self.list_widget.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "English Dictionary"))
        self.search_bar.setPlaceholderText(_translate("MainWindow", "Search"))
        self.list_widget.setSortingEnabled(True)
        self.edit_button.setText(_translate("MainWindow", "Edit"))
        self.delete_button.setText(_translate("MainWindow", "Delete"))
