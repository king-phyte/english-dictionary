# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'definition_groupbox.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DefinitionGroupBox(object):
    def setupUi(self, DefinitionGroupBox):
        DefinitionGroupBox.setObjectName("DefinitionGroupBox")
        DefinitionGroupBox.resize(400, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(DefinitionGroupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(DefinitionGroupBox)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.definitions_layout = QtWidgets.QFormLayout(self.groupBox)
        self.definitions_layout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.definitions_layout.setObjectName("definitions_layout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.definitions_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.definition_lineedit = QtWidgets.QLineEdit(self.groupBox)
        self.definition_lineedit.setClearButtonEnabled(True)
        self.definition_lineedit.setObjectName("definition_lineedit")
        self.definitions_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.definition_lineedit)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.definitions_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.example_lineedit = QtWidgets.QLineEdit(self.groupBox)
        self.example_lineedit.setClearButtonEnabled(True)
        self.example_lineedit.setObjectName("example_lineedit")
        self.definitions_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.example_lineedit)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.definitions_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.related_words_groupbox_layout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.related_words_groupbox_layout.setObjectName("related_words_groupbox_layout")
        self.add_related_words_button = QtWidgets.QPushButton(self.groupBox_2)
        self.add_related_words_button.setObjectName("add_related_words_button")
        self.related_words_groupbox_layout.addWidget(self.add_related_words_button, 0, QtCore.Qt.AlignRight)
        self.definitions_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.groupBox_2)
        self.horizontalLayout.addWidget(self.groupBox)

        self.retranslateUi(DefinitionGroupBox)
        QtCore.QMetaObject.connectSlotsByName(DefinitionGroupBox)

    def retranslateUi(self, DefinitionGroupBox):
        _translate = QtCore.QCoreApplication.translate
        DefinitionGroupBox.setWindowTitle(_translate("DefinitionGroupBox", "Form"))
        self.label.setText(_translate("DefinitionGroupBox", "Definition"))
        self.definition_lineedit.setPlaceholderText(_translate("DefinitionGroupBox", "the male ruler of an independent state, especially one who inherits the position by right of birth."))
        self.label_2.setText(_translate("DefinitionGroupBox", "Example"))
        self.example_lineedit.setPlaceholderText(_translate("DefinitionGroupBox", "King Henry VIII"))
        self.label_3.setText(_translate("DefinitionGroupBox", "Related Words"))
        self.add_related_words_button.setToolTip(_translate("DefinitionGroupBox", "Add another related words form"))
        self.add_related_words_button.setText(_translate("DefinitionGroupBox", "Add Related Words"))
