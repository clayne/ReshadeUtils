#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from src.main_src import MainSrc
from src.utils import constants
from src import resources_rc


class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(1000, 700)
        Main.setMinimumSize(QtCore.QSize(1000, 700))
        Main.setMaximumSize(QtCore.QSize(1000, 700))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        Main.setFont(font)
        self.reshade_version_label = QtWidgets.QLabel(Main)
        self.reshade_version_label.setGeometry(QtCore.QRect(860, 10, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.reshade_version_label.setFont(font)
        self.reshade_version_label.setText("")
        self.reshade_version_label.setAlignment(QtCore.Qt.AlignCenter)
        self.reshade_version_label.setObjectName("reshade_version_label")
        self.main_tabWidget = QtWidgets.QTabWidget(Main)
        self.main_tabWidget.setGeometry(QtCore.QRect(20, 10, 961, 641))
        self.main_tabWidget.setIconSize(QtCore.QSize(20, 20))
        self.main_tabWidget.setUsesScrollButtons(False)
        self.main_tabWidget.setObjectName("main_tabWidget")
        self.games_tab = QtWidgets.QWidget()
        self.games_tab.setObjectName("games_tab")
        self.add_button = QtWidgets.QPushButton(self.games_tab)
        self.add_button.setGeometry(QtCore.QRect(40, 560, 160, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.add_button.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/images/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_button.setIcon(icon)
        self.add_button.setObjectName("add_button")
        self.edit_path_button = QtWidgets.QPushButton(self.games_tab)
        self.edit_path_button.setGeometry(QtCore.QRect(550, 560, 160, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.edit_path_button.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/resources/images/arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.edit_path_button.setIcon(icon1)
        self.edit_path_button.setObjectName("edit_path_button")
        self.delete_button = QtWidgets.QPushButton(self.games_tab)
        self.delete_button.setGeometry(QtCore.QRect(210, 560, 160, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.delete_button.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/resources/images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_button.setIcon(icon2)
        self.delete_button.setObjectName("delete_button")
        self.apply_button = QtWidgets.QPushButton(self.games_tab)
        self.apply_button.setGeometry(QtCore.QRect(780, 560, 160, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.apply_button.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/resources/images/apply.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.apply_button.setIcon(icon3)
        self.apply_button.setObjectName("apply_button")
        self.programs_tableWidget = QtWidgets.QTableWidget(self.games_tab)
        self.programs_tableWidget.setGeometry(QtCore.QRect(0, 0, 961, 541))
        self.programs_tableWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.programs_tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.programs_tableWidget.setAutoScroll(False)
        self.programs_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.programs_tableWidget.setDragDropOverwriteMode(False)
        self.programs_tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.programs_tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.programs_tableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.programs_tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.programs_tableWidget.setWordWrap(False)
        self.programs_tableWidget.setCornerButtonEnabled(False)
        self.programs_tableWidget.setColumnCount(4)
        self.programs_tableWidget.setObjectName("programs_tableWidget")
        self.programs_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.programs_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.programs_tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.programs_tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.programs_tableWidget.setHorizontalHeaderItem(3, item)
        self.programs_tableWidget.horizontalHeader().setVisible(True)
        self.programs_tableWidget.horizontalHeader().setDefaultSectionSize(120)
        self.programs_tableWidget.horizontalHeader().setHighlightSections(False)
        self.programs_tableWidget.horizontalHeader().setMinimumSectionSize(120)
        self.programs_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.programs_tableWidget.verticalHeader().setVisible(True)
        self.programs_tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.programs_tableWidget.verticalHeader().setMinimumSectionSize(30)
        self.edit_preset_button = QtWidgets.QPushButton(self.games_tab)
        self.edit_preset_button.setGeometry(QtCore.QRect(380, 560, 160, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.edit_preset_button.setFont(font)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/resources/images/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.edit_preset_button.setIcon(icon4)
        self.edit_preset_button.setObjectName("edit_preset_button")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/resources/images/controller.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.main_tabWidget.addTab(self.games_tab, icon5, "")
        self.settings_tab = QtWidgets.QWidget()
        self.settings_tab.setObjectName("settings_tab")
        self.update_shaders_groupBox = QtWidgets.QGroupBox(self.settings_tab)
        self.update_shaders_groupBox.setGeometry(QtCore.QRect(100, 40, 330, 60))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.update_shaders_groupBox.setFont(font)
        self.update_shaders_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.update_shaders_groupBox.setObjectName("update_shaders_groupBox")
        self.yes_update_shaders_radioButton = QtWidgets.QRadioButton(self.update_shaders_groupBox)
        self.yes_update_shaders_radioButton.setGeometry(QtCore.QRect(200, 30, 50, 20))
        self.yes_update_shaders_radioButton.setObjectName("yes_update_shaders_radioButton")
        self.no_update_shaders_radioButton = QtWidgets.QRadioButton(self.update_shaders_groupBox)
        self.no_update_shaders_radioButton.setGeometry(QtCore.QRect(90, 30, 50, 20))
        self.no_update_shaders_radioButton.setObjectName("no_update_shaders_radioButton")
        self.check_program_updates_groupBox = QtWidgets.QGroupBox(self.settings_tab)
        self.check_program_updates_groupBox.setGeometry(QtCore.QRect(500, 180, 330, 60))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.check_program_updates_groupBox.setFont(font)
        self.check_program_updates_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.check_program_updates_groupBox.setObjectName("check_program_updates_groupBox")
        self.yes_check_program_updates_radioButton = QtWidgets.QRadioButton(self.check_program_updates_groupBox)
        self.yes_check_program_updates_radioButton.setGeometry(QtCore.QRect(200, 30, 50, 20))
        self.yes_check_program_updates_radioButton.setObjectName("yes_check_program_updates_radioButton")
        self.no_check_program_updates_radioButton = QtWidgets.QRadioButton(self.check_program_updates_groupBox)
        self.no_check_program_updates_radioButton.setGeometry(QtCore.QRect(90, 30, 50, 20))
        self.no_check_program_updates_radioButton.setObjectName("no_check_program_updates_radioButton")
        self.use_dark_theme_groupBox = QtWidgets.QGroupBox(self.settings_tab)
        self.use_dark_theme_groupBox.setGeometry(QtCore.QRect(500, 40, 330, 60))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.use_dark_theme_groupBox.setFont(font)
        self.use_dark_theme_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.use_dark_theme_groupBox.setObjectName("use_dark_theme_groupBox")
        self.yes_dark_theme_radioButton = QtWidgets.QRadioButton(self.use_dark_theme_groupBox)
        self.yes_dark_theme_radioButton.setGeometry(QtCore.QRect(200, 30, 50, 20))
        self.yes_dark_theme_radioButton.setObjectName("yes_dark_theme_radioButton")
        self.no_dark_theme_radioButton = QtWidgets.QRadioButton(self.use_dark_theme_groupBox)
        self.no_dark_theme_radioButton.setGeometry(QtCore.QRect(90, 30, 50, 20))
        self.no_dark_theme_radioButton.setObjectName("no_dark_theme_radioButton")
        self.create_screenshots_folder_groupBox = QtWidgets.QGroupBox(self.settings_tab)
        self.create_screenshots_folder_groupBox.setGeometry(QtCore.QRect(100, 110, 330, 60))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.create_screenshots_folder_groupBox.setFont(font)
        self.create_screenshots_folder_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.create_screenshots_folder_groupBox.setObjectName("create_screenshots_folder_groupBox")
        self.yes_screenshots_folder_radioButton = QtWidgets.QRadioButton(self.create_screenshots_folder_groupBox)
        self.yes_screenshots_folder_radioButton.setGeometry(QtCore.QRect(200, 30, 50, 20))
        self.yes_screenshots_folder_radioButton.setObjectName("yes_screenshots_folder_radioButton")
        self.no_screenshots_folder_radioButton = QtWidgets.QRadioButton(self.create_screenshots_folder_groupBox)
        self.no_screenshots_folder_radioButton.setGeometry(QtCore.QRect(90, 30, 50, 20))
        self.no_screenshots_folder_radioButton.setObjectName("no_screenshots_folder_radioButton")
        self.check_reshade_updates_groupBox = QtWidgets.QGroupBox(self.settings_tab)
        self.check_reshade_updates_groupBox.setGeometry(QtCore.QRect(100, 180, 330, 60))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.check_reshade_updates_groupBox.setFont(font)
        self.check_reshade_updates_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.check_reshade_updates_groupBox.setObjectName("check_reshade_updates_groupBox")
        self.yes_check_reshade_updates_radioButton = QtWidgets.QRadioButton(self.check_reshade_updates_groupBox)
        self.yes_check_reshade_updates_radioButton.setGeometry(QtCore.QRect(200, 30, 50, 20))
        self.yes_check_reshade_updates_radioButton.setObjectName("yes_check_reshade_updates_radioButton")
        self.no_check_reshade_updates_radioButton = QtWidgets.QRadioButton(self.check_reshade_updates_groupBox)
        self.no_check_reshade_updates_radioButton.setGeometry(QtCore.QRect(90, 30, 50, 20))
        self.no_check_reshade_updates_radioButton.setObjectName("no_check_reshade_updates_radioButton")
        self.silent_reshade_updates_groupBox = QtWidgets.QGroupBox(self.settings_tab)
        self.silent_reshade_updates_groupBox.setGeometry(QtCore.QRect(100, 250, 330, 60))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.silent_reshade_updates_groupBox.setFont(font)
        self.silent_reshade_updates_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.silent_reshade_updates_groupBox.setObjectName("silent_reshade_updates_groupBox")
        self.yes_silent_reshade_updates_radioButton = QtWidgets.QRadioButton(self.silent_reshade_updates_groupBox)
        self.yes_silent_reshade_updates_radioButton.setGeometry(QtCore.QRect(200, 30, 50, 20))
        self.yes_silent_reshade_updates_radioButton.setObjectName("yes_silent_reshade_updates_radioButton")
        self.no_silent_reshade_updates_radioButton = QtWidgets.QRadioButton(self.silent_reshade_updates_groupBox)
        self.no_silent_reshade_updates_radioButton.setGeometry(QtCore.QRect(90, 30, 50, 20))
        self.no_silent_reshade_updates_radioButton.setObjectName("no_silent_reshade_updates_radioButton")
        self.show_info_messages_groupBox = QtWidgets.QGroupBox(self.settings_tab)
        self.show_info_messages_groupBox.setGeometry(QtCore.QRect(500, 110, 331, 60))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.show_info_messages_groupBox.setFont(font)
        self.show_info_messages_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.show_info_messages_groupBox.setObjectName("show_info_messages_groupBox")
        self.no_show_info_messages_radioButton = QtWidgets.QRadioButton(self.show_info_messages_groupBox)
        self.no_show_info_messages_radioButton.setGeometry(QtCore.QRect(90, 30, 50, 20))
        self.no_show_info_messages_radioButton.setObjectName("no_show_info_messages_radioButton")
        self.yes_show_info_messages_radioButton = QtWidgets.QRadioButton(self.show_info_messages_groupBox)
        self.yes_show_info_messages_radioButton.setGeometry(QtCore.QRect(200, 30, 50, 20))
        self.yes_show_info_messages_radioButton.setObjectName("yes_show_info_messages_radioButton")
        self.reset_all_button = QtWidgets.QPushButton(self.settings_tab)
        self.reset_all_button.setGeometry(QtCore.QRect(500, 300, 330, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.reset_all_button.setFont(font)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/resources/images/reset.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reset_all_button.setIcon(icon6)
        self.reset_all_button.setIconSize(QtCore.QSize(27, 27))
        self.reset_all_button.setObjectName("reset_all_button")
        self.edit_default_preset_plugin_button = QtWidgets.QPushButton(self.settings_tab)
        self.edit_default_preset_plugin_button.setGeometry(QtCore.QRect(500, 260, 330, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit_default_preset_plugin_button.sizePolicy().hasHeightForWidth())
        self.edit_default_preset_plugin_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.edit_default_preset_plugin_button.setFont(font)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/resources/images/plugin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.edit_default_preset_plugin_button.setIcon(icon7)
        self.edit_default_preset_plugin_button.setObjectName("edit_default_preset_plugin_button")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/resources/images/gear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.main_tabWidget.addTab(self.settings_tab, icon8, "")
        self.about_tab = QtWidgets.QWidget()
        self.about_tab.setObjectName("about_tab")
        self.about_textBrowser = QtWidgets.QTextBrowser(self.about_tab)
        self.about_textBrowser.setGeometry(QtCore.QRect(0, 0, 961, 611))
        self.about_textBrowser.setAcceptDrops(False)
        self.about_textBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.about_textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.about_textBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.about_textBrowser.setUndoRedoEnabled(False)
        self.about_textBrowser.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.about_textBrowser.setOpenExternalLinks(True)
        self.about_textBrowser.setObjectName("about_textBrowser")
        self.donate_button = QtWidgets.QPushButton(self.about_tab)
        self.donate_button.setGeometry(QtCore.QRect(360, 20, 230, 90))
        self.donate_button.setMinimumSize(QtCore.QSize(230, 90))
        self.donate_button.setMaximumSize(QtCore.QSize(230, 90))
        self.donate_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.donate_button.setToolTip("Donate")
        self.donate_button.setAutoFillBackground(False)
        self.donate_button.setStyleSheet("#donate_button {\n"
"    background-color: transparent;\n"
"    background: none;\n"
"    border: none;\n"
"    background-repeat: none;\n"
"}")
        self.donate_button.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/resources/images/donate.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.donate_button.setIcon(icon9)
        self.donate_button.setIconSize(QtCore.QSize(100, 100))
        self.donate_button.setObjectName("donate_button")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/resources/images/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.main_tabWidget.addTab(self.about_tab, icon10, "")
        self.updateAvail_label = QtWidgets.QLabel(Main)
        self.updateAvail_label.setGeometry(QtCore.QRect(260, 655, 481, 40))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.updateAvail_label.setFont(font)
        self.updateAvail_label.setText("")
        self.updateAvail_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.updateAvail_label.setObjectName("updateAvail_label")
        self.update_button = QtWidgets.QPushButton(Main)
        self.update_button.setGeometry(QtCore.QRect(820, 660, 130, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.update_button.setFont(font)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/resources/images/update.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.update_button.setIcon(icon11)
        self.update_button.setObjectName("update_button")
        self.main_tabWidget.raise_()
        self.updateAvail_label.raise_()
        self.update_button.raise_()
        self.reshade_version_label.raise_()

        self.retranslateUi(Main)
        QtCore.QMetaObject.connectSlotsByName(Main)

        main_src = MainSrc(self, Main)
        main_src.start()


    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate("Main", constants.FULL_PROGRAM_NAME))
        self.add_button.setToolTip(_translate("Main", "Add a game"))
        self.add_button.setText(_translate("Main", "ADD"))
        self.edit_path_button.setToolTip(_translate("Main", "Edit the selected game path"))
        self.edit_path_button.setText(_translate("Main", "EDIT LOCATION"))
        self.delete_button.setToolTip(_translate("Main", "Delete the selected game"))
        self.delete_button.setText(_translate("Main", "DELETE"))
        self.apply_button.setToolTip(_translate("Main", "Apply Reshade to All Games"))
        self.apply_button.setText(_translate("Main", "APPLY"))
        self.programs_tableWidget.setSortingEnabled(True)
        item = self.programs_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Main", "NAME"))
        item = self.programs_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Main", "ARCHITECTURE"))
        item = self.programs_tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Main", "API"))
        item = self.programs_tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Main", "LOCATION"))
        self.edit_preset_button.setToolTip(_translate("Main", "Edit the selected reshade preset file"))
        self.edit_preset_button.setText(_translate("Main", "EDIT PRESET FILE"))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.games_tab), _translate("Main", "GAMES"))
        self.update_shaders_groupBox.setToolTip(_translate("Main", "Update Shader Files Everytime on Apply"))
        self.update_shaders_groupBox.setTitle(_translate("Main", "Always Update Shader Files"))
        self.yes_update_shaders_radioButton.setText(_translate("Main", "YES"))
        self.no_update_shaders_radioButton.setText(_translate("Main", "NO"))
        self.check_program_updates_groupBox.setTitle(_translate("Main", "Check for Program Updates on Startup"))
        self.yes_check_program_updates_radioButton.setText(_translate("Main", "YES"))
        self.no_check_program_updates_radioButton.setText(_translate("Main", "NO"))
        self.use_dark_theme_groupBox.setTitle(_translate("Main", "Use Dark Theme"))
        self.yes_dark_theme_radioButton.setText(_translate("Main", "YES"))
        self.no_dark_theme_radioButton.setText(_translate("Main", "NO"))
        self.create_screenshots_folder_groupBox.setTitle(_translate("Main", "Create Screenshot Folders"))
        self.yes_screenshots_folder_radioButton.setText(_translate("Main", "YES"))
        self.no_screenshots_folder_radioButton.setText(_translate("Main", "NO"))
        self.check_reshade_updates_groupBox.setTitle(_translate("Main", "Check for Reshade Updates on Startup"))
        self.yes_check_reshade_updates_radioButton.setText(_translate("Main", "YES"))
        self.no_check_reshade_updates_radioButton.setText(_translate("Main", "NO"))
        self.silent_reshade_updates_groupBox.setTitle(_translate("Main", "Silent Reshade Updates"))
        self.yes_silent_reshade_updates_radioButton.setText(_translate("Main", "YES"))
        self.no_silent_reshade_updates_radioButton.setText(_translate("Main", "NO"))
        self.show_info_messages_groupBox.setTitle(_translate("Main", "Always Show Info and Confirmation Messages"))
        self.no_show_info_messages_radioButton.setText(_translate("Main", "NO"))
        self.yes_show_info_messages_radioButton.setText(_translate("Main", "YES"))
        self.reset_all_button.setToolTip(_translate("Main", "Reset all reshade configs to default"))
        self.reset_all_button.setText(_translate("Main", "RESET ALL RESHADE CONFIGS TO DEAFULT"))
        self.edit_default_preset_plugin_button.setToolTip(_translate("Main", "Edit default preset plugins config file"))
        self.edit_default_preset_plugin_button.setText(_translate("Main", "EDIT DEFAULT PRESET PLUGINS CONFIG FILE"))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.settings_tab), _translate("Main", "SETTINGS"))
        self.about_textBrowser.setHtml(_translate("Main", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:6pt;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:6pt;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:6pt;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:6pt;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:6pt;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:6pt;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:6pt;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:6pt;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:6pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Reshade Utilities</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Program to copy reshade DLLs, shaders and config fiies to several games</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Developed as an open source project and hosted on GitHub</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Implemented using Python3, PyQt5 and SQLite3</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt; text-decoration: underline; color:#0000ff;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Acknowledgements</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://riverbankcomputing.com/software/pyqt/download\"><span style=\" font-size:11pt; text-decoration: underline; color:#8b0000;\">PyQt5</span></a></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://www.python.org\"><span style=\" font-size:11pt; text-decoration: underline; color:#8b0000;\">Python3</span></a></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://reshade.me/\"><span style=\" font-size:11pt; text-decoration: underline; color:#8b0000;\">Reshade</span></a></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://pyinstaller.readthedocs.io\"><span style=\" font-size:11pt; text-decoration: underline; color:#8b0000;\">PyInstaller</span></a></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt; text-decoration: underline; color:#0000ff;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Developed by ddc</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"mailto:dddcsta@gmail.com\"><span style=\" font-size:11pt; text-decoration: underline; color:#8b0000;\">Email</span></a></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://github.com/ddc/ReshadeUtils/releases/latest\"><span style=\" font-size:11pt; text-decoration: underline; color:#8b0000;\">Download</span></a></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.about_tab), _translate("Main", "ABOUT"))
        self.update_button.setToolTip(_translate("Main", "Update program version"))
        self.update_button.setText(_translate("Main", "UPDATE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Main = QtWidgets.QWidget()
    ui = Ui_Main()
    ui.setupUi(Main)
    Main.show()
    sys.exit(app.exec_())
