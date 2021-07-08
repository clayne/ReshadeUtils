# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

import os
import requests
from src.log import Log
from PyQt5.QtCore import Qt
from bs4 import BeautifulSoup
from src.config import Ui_config
from src.sql.games_sql import GamesSql
from src.progressbar import ProgressBar
from src.sql.config_sql import ConfigSql
from src.sql.database import DatabaseClass
from PyQt5 import QtWidgets
from src import constants, events, messages, utils, qtutils


class MainSrc:
    def __init__(self, qtobj, form):
        self.qtobj = qtobj
        self.form = form
        self.client_version = constants.VERSION
        self.log = Log().setup_logging()
        self.database = DatabaseClass(self.log)
        self.progressbar = ProgressBar()
        self.need_apply = False
        self.selected_game = None
        self.game_config_form = None
        self.reshade_version = None
        self.local_reshade_path = None
        self.use_dark_theme = None
        self.update_shaders = None
        self.check_program_updates = None
        self.check_reshade_updates = None
        self.silent_reshade_updates = None
        self.create_screenshots_folder = None
        self.new_version = None
        self.remote_reshade_version = None
        self.remote_reshade_download_url = None
        self.show_info_messages = None


    def start(self):
        utils.check_dirs()
        self.log.info(f"STARTING {constants.FULL_PROGRAM_NAME}")

        self.progressbar.set_values(messages.checking_db_connection, 15)
        utils.check_db_connection(self)
        utils.create_default_tables(self)

        self.progressbar.set_values(messages.checking_db_connection, 30)
        utils.check_database_configs(self)

        self.progressbar.set_values(messages.checking_files, 45)
        self.check_reshade_files()
        utils.download_shaders(self)
        self.set_ui_var_configs()

        self.progressbar.set_values(messages.checking_new_reshade_version, 60)
        self.get_remote_reshade_version()

        self.progressbar.set_values(messages.checking_configs, 75)
        self.register_form_events()

        self.progressbar.set_values(messages.checking_new_version, 90)
        self.check_new_program_version()

        self.qtobj.main_tabWidget.setCurrentIndex(0)
        self.qtobj.programs_tableWidget.setColumnWidth(2, 130)
        self.qtobj.programs_tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        self.progressbar.close()
        self.populate_datagrid()
        self.enable_widgets(False)


    def set_ui_var_configs(self):
        config_sql = ConfigSql(self)
        rs_config = config_sql.get_configs()
        if rs_config is not None and len(rs_config) > 0:
            if not rs_config[0].get("use_dark_theme"):
                self.use_dark_theme = False
                self.set_style_sheet(False)
                self.qtobj.yes_dark_theme_radioButton.setChecked(False)
                self.qtobj.no_dark_theme_radioButton.setChecked(True)
            else:
                self.use_dark_theme = True
                self.set_style_sheet(True)
                self.qtobj.yes_dark_theme_radioButton.setChecked(True)
                self.qtobj.no_dark_theme_radioButton.setChecked(False)

            if not rs_config[0].get("show_info_messages"):
                self.show_info_messages = False
                self.qtobj.yes_show_info_messages_radioButton.setChecked(False)
                self.qtobj.no_show_info_messages_radioButton.setChecked(True)
            else:
                self.show_info_messages = True
                self.qtobj.yes_show_info_messages_radioButton.setChecked(True)
                self.qtobj.no_show_info_messages_radioButton.setChecked(False)

            if not rs_config[0].get("update_shaders"):
                self.update_shaders = False
                self.qtobj.yes_update_shaders_radioButton.setChecked(False)
                self.qtobj.no_update_shaders_radioButton.setChecked(True)
            else:
                self.update_shaders = True
                self.qtobj.yes_update_shaders_radioButton.setChecked(True)
                self.qtobj.no_update_shaders_radioButton.setChecked(False)

            if not rs_config[0].get("check_program_updates"):
                self.check_program_updates = False
                self.qtobj.yes_check_program_updates_radioButton.setChecked(False)
                self.qtobj.no_check_program_updates_radioButton.setChecked(True)
            else:
                self.check_program_updates = True
                self.qtobj.yes_check_program_updates_radioButton.setChecked(True)
                self.qtobj.no_check_program_updates_radioButton.setChecked(False)

            if not rs_config[0].get("check_reshade_updates"):
                self.check_reshade_updates = False
                self.qtobj.yes_check_reshade_updates_radioButton.setChecked(False)
                self.qtobj.no_check_reshade_updates_radioButton.setChecked(True)
            else:
                self.check_reshade_updates = True
                self.qtobj.yes_check_reshade_updates_radioButton.setChecked(True)
                self.qtobj.no_check_reshade_updates_radioButton.setChecked(False)

            if not rs_config[0].get("create_screenshots_folder"):
                self.create_screenshots_folder = False
                self.qtobj.yes_screenshots_folder_radioButton.setChecked(False)
                self.qtobj.no_screenshots_folder_radioButton.setChecked(True)
            else:
                self.create_screenshots_folder = True
                self.qtobj.yes_screenshots_folder_radioButton.setChecked(True)
                self.qtobj.no_screenshots_folder_radioButton.setChecked(False)

            if not rs_config[0].get("silent_reshade_updates"):
                self.silent_reshade_updates = False
                self.qtobj.yes_silent_reshade_updates_radioButton.setChecked(False)
                self.qtobj.no_silent_reshade_updates_radioButton.setChecked(True)
            else:
                self.silent_reshade_updates = True
                self.qtobj.yes_silent_reshade_updates_radioButton.setChecked(True)
                self.qtobj.no_silent_reshade_updates_radioButton.setChecked(False)
            self.qtobj.silent_reshade_updates_groupBox.setEnabled(self.check_reshade_updates)
            self.qtobj.silent_reshade_updates_groupBox.setVisible(self.check_reshade_updates)


    def register_form_events(self):
        # TAB 1 - games
        self.qtobj.add_button.clicked.connect(lambda: events.add_game(self))
        self.qtobj.delete_button.clicked.connect(lambda: events.delete_game(self))
        self.qtobj.edit_path_button.clicked.connect(lambda: events.edit_game_path(self))
        self.qtobj.edit_preset_button.clicked.connect(lambda: events.open_preset_config_file(self))
        self.qtobj.apply_button.clicked.connect(lambda: events.apply_all(self))
        self.qtobj.update_button.clicked.connect(lambda: events.update_clicked())
        self.qtobj.programs_tableWidget.clicked.connect(self._programs_table_widget_clicked)
        self.qtobj.programs_tableWidget.itemDoubleClicked.connect(self._programs_table_widget_double_clicked)

        # TAB 2 - configs
        self.qtobj.yes_dark_theme_radioButton.clicked.connect(lambda: events.dark_theme_clicked(self, "YES"))
        self.qtobj.no_dark_theme_radioButton.clicked.connect(lambda: events.dark_theme_clicked(self, "NO"))

        self.qtobj.yes_check_program_updates_radioButton.clicked.connect(lambda: events.check_program_updates_clicked(self, "YES"))
        self.qtobj.no_check_program_updates_radioButton.clicked.connect(lambda: events.check_program_updates_clicked(self, "NO"))

        self.qtobj.yes_show_info_messages_radioButton.clicked.connect(lambda: events.show_info_messages_clicked(self, "YES"))
        self.qtobj.no_show_info_messages_radioButton.clicked.connect(lambda: events.show_info_messages_clicked(self, "NO"))

        self.qtobj.yes_check_reshade_updates_radioButton.clicked.connect(lambda: events.check_reshade_updates_clicked(self, "YES"))
        self.qtobj.no_check_reshade_updates_radioButton.clicked.connect(lambda: events.check_reshade_updates_clicked(self, "NO"))

        self.qtobj.yes_silent_reshade_updates_radioButton.clicked.connect(lambda: events.silent_reshade_updates_clicked(self, "YES"))
        self.qtobj.no_silent_reshade_updates_radioButton.clicked.connect(lambda: events.silent_reshade_updates_clicked(self, "NO"))

        self.qtobj.yes_update_shaders_radioButton.clicked.connect(lambda: events.update_shaders_clicked(self, "YES"))
        self.qtobj.no_update_shaders_radioButton.clicked.connect(lambda: events.update_shaders_clicked(self, "NO"))

        self.qtobj.yes_screenshots_folder_radioButton.clicked.connect(lambda: events.create_screenshots_folder_clicked(self, "YES"))
        self.qtobj.no_screenshots_folder_radioButton.clicked.connect(lambda: events.create_screenshots_folder_clicked(self, "NO"))

        self.qtobj.edit_default_preset_plugin_button.clicked.connect(lambda: events.edit_default_preset_plugin_button_clicked(self))
        self.qtobj.reset_all_button.clicked.connect(lambda: events.reset_all_button_clicked(self))

        # TAB 3 - about
        self.qtobj.donate_button.clicked.connect(lambda: events.donate_clicked())


    def get_remote_reshade_version(self):
        self.remote_reshade_version = None
        self.remote_reshade_download_url = None

        if self.check_reshade_updates:
            try:
                response = requests.get(constants.RESHADE_WEBSITE_URL)
                if response.status_code != 200:
                    self.log.error(messages.reshade_page_error)
                else:
                    html = str(response.text)
                    soup = BeautifulSoup(html, "html.parser")
                    body = soup.body
                    blist = str(body).split("<p>")

                    for content in blist:
                        if content.startswith("<strong>Version "):
                            self.remote_reshade_version = content.split()[1].strip("</strong>")
                            self.remote_reshade_download_url = f"{constants.RESHADE_EXE_URL}{self.remote_reshade_version}.exe"
                            break

                    if self.remote_reshade_version != self.reshade_version:
                        self.need_apply = True
                        if not self.silent_reshade_updates:
                            msg = messages.update_reshade_question
                            reply = qtutils.show_message_window(self.log, "question", msg)
                            if reply == QtWidgets.QMessageBox.Yes:
                                self._download_reshade()
                        else:
                            self._download_reshade()

            except requests.exceptions.ConnectionError as e:
                self.log.error(f"{messages.reshade_website_unreacheable} {str(e)}")
                qtutils.show_message_window(self.log, "error", messages.reshade_website_unreacheable)
                return


    def check_reshade_files(self):
        utils.create_local_reshade_files(self)
        config_sql = ConfigSql(self)
        rs_config = config_sql.get_configs()
        if rs_config is not None and rs_config[0].get("reshade_version") is not None:
            self.reshade_version = rs_config[0].get("reshade_version")
            self.local_reshade_path = os.path.join(constants.PROGRAM_PATH, f"ReShade_Setup_{self.reshade_version}.exe")
            self.qtobj.reshade_version_label.setText(f"{messages.info_reshade_version}{self.reshade_version}")
            self.enable_form(True)


    def check_new_program_version(self):
        self.qtobj.update_button.setVisible(False)
        if self.check_program_updates:
            new_version_obj = utils.check_new_program_version(self)
            if new_version_obj.new_version_available:
                self.qtobj.updateAvail_label.clear()
                self.qtobj.updateAvail_label.setText(new_version_obj.new_version_msg)
                self.qtobj.update_button.setVisible(True)


    def show_game_config_form(self, game_name, architecture):
        if not utils.check_game_file(self):
            qtutils.show_message_window(self.log, "error", messages.error_game_not_found)
            return

        self.game_config_form = QtWidgets.QWidget()
        qt_obj = Ui_config()
        qt_obj.setupUi(self.game_config_form)
        self.game_config_form.qtObj = qt_obj

        if self.use_dark_theme:
            self.game_config_form.setStyleSheet(open(constants.QSS_FILENAME, "r").read())

        self.game_config_form.qtObj.game_name_lineEdit.setFocus()
        self.game_config_form.show()
        QtWidgets.QApplication.processEvents()

        self.game_config_form.qtObj.ok_pushButton.clicked.connect(lambda: events.game_config_form_result(self, architecture, "OK"))
        self.game_config_form.qtObj.cancel_pushButton.clicked.connect(lambda: events.game_config_form_result(self, architecture, "CANCEL"))

        if self.selected_game is not None:
            self.game_config_form.qtObj.game_name_lineEdit.setText(self.selected_game.name)
            if self.selected_game.api == constants.DX9_DISPLAY_NAME:
                self.game_config_form.qtObj.dx9_radioButton.setChecked(True)
                self.game_config_form.qtObj.dx_radioButton.setChecked(False)
                self.game_config_form.qtObj.opengl_radioButton.setChecked(False)
            elif self.selected_game.api == constants.OPENGL_DISPLAY_NAME:
                self.game_config_form.qtObj.dx9_radioButton.setChecked(False)
                self.game_config_form.qtObj.dx_radioButton.setChecked(False)
                self.game_config_form.qtObj.opengl_radioButton.setChecked(True)
            else:
                self.game_config_form.qtObj.dx9_radioButton.setChecked(False)
                self.game_config_form.qtObj.dx_radioButton.setChecked(True)
                self.game_config_form.qtObj.opengl_radioButton.setChecked(False)
        else:
            self.game_config_form.qtObj.game_name_lineEdit.setText(game_name)


    def set_style_sheet(self, status: bool):
        if status:
            self.form.setStyleSheet(open(constants.QSS_FILENAME, "r").read())
        else:
            self.form.setStyleSheet("")


    def populate_datagrid(self):
        self.qtobj.programs_tableWidget.setRowCount(0) # cleanning datagrid
        games_sql = GamesSql(self)
        rs_all_games = games_sql.get_games()
        if rs_all_games is not None and len(rs_all_games) > 0:
            for i in range(len(rs_all_games)):
                self.qtobj.programs_tableWidget.insertRow(i)
                self.qtobj.programs_tableWidget.setItem(i, 0,
                                                        QtWidgets.QTableWidgetItem(rs_all_games[i].get("name")))
                self.qtobj.programs_tableWidget.setItem(i, 1,
                                                        QtWidgets.QTableWidgetItem(rs_all_games[i].get("architecture")))
                self.qtobj.programs_tableWidget.setItem(i, 2,
                                                        QtWidgets.QTableWidgetItem(rs_all_games[i].get("api")))
                self.qtobj.programs_tableWidget.setItem(i, 3,
                                                        QtWidgets.QTableWidgetItem(rs_all_games[i].get("path")))

        self.qtobj.programs_tableWidget.resizeColumnsToContents()
        highest_column_width = self.qtobj.programs_tableWidget.columnWidth(3)
        if highest_column_width < 600:
            self.qtobj.programs_tableWidget.horizontalHeader().setStretchLastSection(True)
        else:
            self.qtobj.programs_tableWidget.horizontalHeader().setStretchLastSection(False)
            self.qtobj.programs_tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)


    def enable_form(self, status: bool):
        if not status:
            self.selected_game = None
        self.qtobj.add_button.setEnabled(status)
        for i in range(0, self.qtobj.main_tabWidget.count()):
            self.qtobj.main_tabWidget.setTabEnabled(i, status)


    def enable_widgets(self, status: bool):
        if not status:
            self.selected_game = None
        self._set_state_apply_button()
        self.qtobj.delete_button.setEnabled(status)
        self.qtobj.edit_path_button.setEnabled(status)
        self.qtobj.edit_preset_button.setEnabled(status)


    def _download_reshade(self):
        self.progressbar.set_values(messages.downloading_new_reshade_version, 75)
        if not self.silent_reshade_updates:
            msg = messages.update_reshade_question
            reply = qtutils.show_message_window(self.log, "question", msg)
            if reply == QtWidgets.QMessageBox.No:
                return

        # removing old version
        if self.reshade_version is not None:
            old_local_reshade_exe = os.path.join(constants.PROGRAM_PATH, f"ReShade_Setup_{self.reshade_version}.exe")
            if os.path.isfile(old_local_reshade_exe):
                self.log.info(messages.removing_old_reshade_file)
                os.remove(old_local_reshade_exe)

        try:
            # downloading new reshade version
            self.local_reshade_path = os.path.join(constants.PROGRAM_PATH, f"ReShade_Setup_{self.remote_reshade_version}.exe")
            r = requests.get(self.remote_reshade_download_url)
            if r.status_code == 200:
                self.log.info(f"{messages.downloading_new_reshade_version}: {self.remote_reshade_version}")
                with open(self.local_reshade_path, "wb") as outfile:
                    outfile.write(r.content)
            else:
                self.log.error(messages.error_check_new_reshade_version)
                return
        except Exception as e:
            if hasattr(e, "errno") and e.errno == 13:
                qtutils.show_message_window(self.log, "error", messages.error_permissionError)
            else:
                self.log.error(f"{messages.error_check_new_reshade_version} {str(e)}")
            return

        self.reshade_version = self.remote_reshade_version
        utils.unzip_reshade(self, self.local_reshade_path)

        # save version to sql table
        config_sql = ConfigSql(self)
        config_sql.update_reshade_version(self.remote_reshade_version)

        # set version label
        self.qtobj.reshade_version_label.clear()
        self.qtobj.reshade_version_label.setText(f"{messages.info_reshade_version}{self.remote_reshade_version}")

        len_games = self.qtobj.programs_tableWidget.rowCount()
        if self.need_apply and len_games > 0:
            events.apply_all(self)
            qtutils.show_message_window(self.log, "info",
                                        f"{messages.new_reshade_version}\n"
                                        f"Version: {self.remote_reshade_version}\n\n"
                                        f"{messages.apply_success}")
            self.need_apply = False


    def _set_state_apply_button(self):
        len_games = self.qtobj.programs_tableWidget.rowCount()
        if len_games == 0:
            self.qtobj.apply_button.setEnabled(False)
        else:
            self.qtobj.apply_button.setEnabled(True)


    def _programs_table_widget_clicked(self, item):
        events.programs_tableWidget_clicked(self, item)


    def _programs_table_widget_double_clicked(self):
        if self.selected_game is not None:
            self.show_game_config_form(self.selected_game.name, self.selected_game.architecture)
