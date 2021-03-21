#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

import os
import shutil
import zipfile
import win32file
import requests
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QDesktopServices
from src.sql.configs_sql import ConfigsSql
from src.sql.games_sql import GamesSql
from src.utils import constants, messages, utilities
from src.utils.create_files import CreateFiles


class FormEvents:
    def __init__(self):
        pass


    @staticmethod
    def donate_clicked():
        href = QtCore.QUrl(constants.PAYPAL_URL)
        QDesktopServices.openUrl(href)


    @staticmethod
    def update_clicked():
        href = QtCore.QUrl(constants.GITHUB_LATEST_VERSION_URL)
        QDesktopServices.openUrl(href)


    def add_game(self):
        game_path = utilities.open_get_filename()
        if game_path is not None:
            file_name = str(game_path.split("/")[-1])
            extension = str(file_name.split(".")[-1])
            tl = game_path.split("/")
            game_path = "\\".join(tl)
            if extension.lower() == "exe":
                games_sql = GamesSql(self)
                rs_name = games_sql.get_game_by_path(game_path)
                if rs_name is not None and len(rs_name) == 0:
                    self.selected_game = None
                    self.added_game_path = game_path
                    binary_type = int(win32file.GetBinaryType(game_path))
                    if binary_type == 6:
                        architecture = "64bits"
                    else:
                        architecture = "32bits"

                    self.show_game_config_form(file_name.replace(".exe", ""), architecture)
                else:
                    if rs_name is not None and len(rs_name) > 0:
                        utilities.show_message_window("error", "ERROR", f"{messages.game_already_exist}\n\n{file_name}")
            else:
                utilities.show_message_window("error", "ERROR", f"{messages.not_valid_game}")


    def delete_game(self):
        game_not_found = False
        if not utilities.check_game_dir(self):
             game_not_found = True

        self.enable_widgets(True)
        if self.selected_game is not None:
            reshade_d3d9_log = f"{constants.D3D9.replace('dll', 'log')}"
            reshade_dxgi_log = f"{constants.DXGI.replace('dll', 'log')}"
            reshade_opengl_log = f"{constants.OPENGL.replace('dll', 'log')}"
            path_list = self.selected_game.path.split("\\")[:-1]
            game_path = '\\'.join(path_list)
            game_name = self.selected_game.name
            err = False

            # remove dll from game path
            if self.selected_game.api.lower() == "opengl":
                reshade_dll = f"{game_path}\\{constants.OPENGL}"
                reshade_log_file = f"{game_path}\\{reshade_opengl_log}"
            elif self.selected_game.api.lower() == "dx9":
                reshade_dll = f"{game_path}\\{constants.D3D9}"
                reshade_log_file = f"{game_path}\\{reshade_d3d9_log}"
            else:
                reshade_dll = f"{game_path}\\{constants.DXGI}"
                reshade_log_file = f"{game_path}\\{reshade_dxgi_log}"

            if os.path.isfile(reshade_dll):
                try:
                    os.remove(reshade_dll)
                except OSError as e:
                    self.log.error(f"remove_file: {str(e)}")
                    err = True
                    utilities.show_message_window("error", "ERROR", f"{messages.error_delete_dll} {game_name} dll\n\n{e.strerror}")

            if not err:
                try:
                    # remove reshade.ini from game path
                    reshade_ini = f"{game_path}\\{constants.RESHADE_INI}"
                    if os.path.isfile(reshade_ini):
                        os.remove(reshade_ini)

                    # remove ReShadePreset.ini from game path
                    reshade_plug_ini = f"{game_path}\\{constants.RESHADE_PRESET_INI}"
                    if os.path.isfile(reshade_plug_ini):
                        os.remove(reshade_plug_ini)

                    # remove Reshade log files from game path
                    if os.path.isfile(reshade_log_file):
                        os.remove(reshade_log_file)

                    # remove from database
                    games_sql = GamesSql(self)
                    games_sql.delete_game(self.selected_game.id)

                    # populate datagrid
                    self.populate_datagrid()
                    if game_not_found:
                        utilities.show_message_window("info", "SUCCESS", f"{messages.game_not_in_path_deleted}\n\n{game_name}")
                    else:
                        utilities.show_message_window("info", "SUCCESS", f"{messages.game_deleted}\n\n{game_name}")
                except OSError as e:
                    self.log.error(f"delete_game: {str(e)}")
                    utilities.show_message_window("error", "ERROR", f"{game_name} files\n\n{e.strerror}")

            self.enable_widgets(False)


    def edit_game_path(self):
        if self.selected_game is not None:
            old_game_path = self.selected_game.path
            new_game_path = utilities.open_get_filename()

            if new_game_path is not None:
                new_game_path = new_game_path.replace("/", "\\")
                if old_game_path == new_game_path:
                    self.enable_widgets(False)
                    utilities.show_message_window("info", "INFO", f"{messages.no_change_path}")
                    return

                old_file_name = str(old_game_path.split("\\")[-1])
                new_file_name = str(new_game_path.split("\\")[-1])
                if old_file_name != new_file_name:
                    self.enable_widgets(False)
                    utilities.show_message_window("error", "ERROR", f"{messages.not_same_game}\n\n{old_file_name}")
                    return

                extension = str(new_file_name.split(".")[-1])
                if extension.lower() != "exe":
                    self.enable_widgets(False)
                    utilities.show_message_window("error", "ERROR", f"{messages.not_valid_game}\n\n{new_file_name}")
                    return

                # save into database
                games_obj = utilities.Object()
                games_sql = GamesSql(self)
                games_obj.id = self.selected_game.id
                games_obj.path = new_game_path
                games_sql.update_game_path(games_obj)

                # create Reshade.ini to replace edit CurrentPresetPath
                game_screenshots_path = _get_screenshot_path(self, new_game_path, self.selected_game.name)
                self.selected_game.game_dir = "\\".join(new_game_path.split("\\")[:-1])

                try:
                    dst_res_ini_path = os.path.join(self.selected_game.game_dir, constants.RESHADE_INI)
                    create_files = CreateFiles(self)
                    create_files.create_reshade_ini_file(dst_res_ini_path, game_screenshots_path)
                except Exception as e:
                    self.log.error(f"create_files: {str(e)}")

                # populate list
                self.populate_datagrid()
                utilities.show_message_window("info", "INFO", f"{messages.path_changed_success}\n\n{new_game_path}")

            self.enable_widgets(False)


    def open_reshade_config_file(self):
        self.enable_widgets(True)
        if self.selected_game is not None:
            path_list = self.selected_game.path.split("\\")[:-1]
            game_path = "\\".join(path_list)
            res_plug_ini_path = f"{game_path}\\{constants.RESHADE_PRESET_INI}"

            try:
                if not os.path.exists(constants.RESHADE_PRESET_FILENAME):
                    create_files = CreateFiles(self)
                    create_files.create_reshade_preset_ini_file()
            except Exception as e:
                self.log.error(f"create_files: {str(e)}")

            try:
                if not os.path.exists(res_plug_ini_path) and os.path.exists(constants.RESHADE_PRESET_FILENAME):
                    shutil.copyfile(constants.RESHADE_PRESET_FILENAME, res_plug_ini_path)
            except Exception as e:
                self.log.error(str(e))

            try:
                os.startfile(f"\"{res_plug_ini_path}\"")
            except Exception as e:
                err_msg = f"{e.strerror}\n\n{messages.check_game_uninstalled}"
                utilities.show_message_window("error", "ERROR", err_msg)

        self.enable_widgets(False)


    def edit_all_games_custom_config_button(self):
        try:
            if not os.path.exists(constants.RESHADE_PRESET_FILENAME):
                create_files = CreateFiles(self)
                create_files.create_reshade_preset_ini_file()
        except Exception as e:
            self.log.error(str(e))

        try:
            os.startfile(f"\"{constants.RESHADE_PRESET_FILENAME}\"")
        except Exception as e:
            err_msg = f"{e.strerror}\n\n{constants.RESHADE_PRESET_INI}{messages.not_found}"
            utilities.show_message_window("error", "ERROR", err_msg)


    def dark_theme_clicked(self, status: str):
        if status == "YES":
            self.set_style_sheet(True)
            self.use_dark_theme = True
            status = 1
        else:
            self.set_style_sheet(False)
            self.use_dark_theme = False
            status = 0

        config_sql = ConfigsSql(self)
        configs_obj = utilities.Object()
        configs_obj.status = status
        config_sql.update_dark_theme(configs_obj)


    def check_program_updates_clicked(self, status: str):
        if status == "YES":
            self.check_program_updates = True
            status = 1
        else:
            self.check_program_updates = False
            status = 0

        config_sql = ConfigsSql(self)
        configs_obj = utilities.Object()
        configs_obj.status = status
        config_sql.update_check_program_updates(configs_obj)


    def check_reshade_updates_clicked(self, status: str):
        if status == "YES":
            self.check_reshade_updates = True
            status = 1
        else:
            self.check_reshade_updates = False
            status = 0

        self.qtobj.silent_reshade_updates_groupBox.setEnabled(self.check_reshade_updates)
        self.qtobj.silent_reshade_updates_groupBox.setVisible(self.check_reshade_updates)

        config_sql = ConfigsSql(self)
        configs_obj = utilities.Object()
        configs_obj.status = status
        config_sql.update_check_resahde_updates(configs_obj)


    def silent_reshade_updates_clicked(self, status: str):
        if status == "YES":
            self.silent_reshade_updates = True
            status = 1
        else:
            self.silent_reshade_updates = False
            status = 0

        config_sql = ConfigsSql(self)
        configs_obj = utilities.Object()
        configs_obj.status = status
        config_sql.update_silent_reshade_updates(configs_obj)


    def update_shaders_clicked(self, status: str):
        if status == "YES":
            self.update_shaders = True
            status = 1
        else:
            self.update_shaders = False
            status = 0

        config_sql = ConfigsSql(self)
        configs_obj = utilities.Object()
        configs_obj.status = status
        config_sql.update_shaders(configs_obj)


    def create_screenshots_folder_clicked(self, status: str):
        if status == "YES":
            self.create_screenshots_folder = True
            status = 1
        else:
            self.create_screenshots_folder = False
            status = 0

        config_sql = ConfigsSql(self)
        configs_obj = utilities.Object()
        configs_obj.status = status
        config_sql.update_create_screenshots_folder(configs_obj)


    def reset_reshade_files_clicked(self, status: str):
        if status == "YES":
            self.reset_reshade_files = True
            status = 1
        else:
            self.reset_reshade_files = False
            status = 0

        config_sql = ConfigsSql(self)
        configs_obj = utilities.Object()
        configs_obj.status = status
        config_sql.update_reset_reshade_files(configs_obj)


    def custom_config_clicked(self, status: str):
        if status == "YES":
            self.use_custom_config = True
            status = 1
        else:
            self.use_custom_config = False
            status = 0

        config_sql = ConfigsSql(self)
        configs_obj = utilities.Object()
        configs_obj.status = status
        config_sql.update_custom_config(configs_obj)


    def programs_tableWidget_clicked(self, item):
        self.enable_widgets(True)
        #clicked_item = self.qtobj.programs_tableWidget.currentItem()
        clicked_row = self.qtobj.programs_tableWidget.selectedItems()

        self.selected_game = utilities.Object()
        #self.selected_game.column = item.column()
        #self.selected_game.row = item.row()
        self.selected_game.name = clicked_row[0].text()
        self.selected_game.architecture = clicked_row[1].text()
        self.selected_game.api = clicked_row[2].text()
        self.selected_game.path = clicked_row[3].text()
        self.selected_game.game_dir = "\\".join(self.selected_game.path.split("\\")[:-1])

        search_pattern = self.selected_game.name
        games_sql = GamesSql(self)
        rs = games_sql.get_game_by_name(search_pattern)
        if rs is not None and len(rs) > 0:
            self.selected_game.id = rs[0].get("id")


    def apply_all(self):
        games_sql = GamesSql(self)
        rs_all_games = games_sql.get_games()
        len_games = len(rs_all_games)
        # len_games = self.qtobj.programs_tableWidget.rowCount()

        if len_games > 0:
            if self.reset_reshade_files:
                msg = f"{messages.reset_config_files_question}"
                reply = utilities.show_message_window("question", "Reset All Configs", msg)
                if reply == QtWidgets.QMessageBox.No:
                    self.reset_reshade_files = False

            if rs_all_games is not None:
                self.enable_form(False)
                self.enable_widgets(False)
                self.qtobj.apply_button.setEnabled(False)

                # download shaders
                _download_shaders(self)

                # begin games update section
                errors = []
                games_obj = utilities.Object()
                self.progressBar.set_values(messages.copying_DLLs, 0)
                for i in range(len(rs_all_games)):
                    self.progressBar.set_values(messages.copying_DLLs, 100 / len_games)
                    games_obj.api = rs_all_games[i]["api"]
                    games_obj.architecture = rs_all_games[i]["architecture"]
                    games_obj.game_name = rs_all_games[i]["name"]
                    games_obj.path = rs_all_games[i]["path"]
                    len_games = len_games - 1
                    result = _apply_single(self, games_obj)
                    if result is not None:
                        errors.append(result)

                self.enable_form(True)
                self.qtobj.apply_button.setEnabled(True)

                if len(errors) == 0 and self.need_apply is False:
                    utilities.show_message_window("info", "SUCCESS", f"{messages.apply_success}")
                elif len(errors) > 0:
                    err = "\n".join(errors)
                    utilities.show_message_window("error", "ERROR", f"{messages.apply_success_with_errors}\n\n{err}")

                self.progressBar.close()


    def game_config_form_result(self, architecture, status):
        if status == "OK":
            self.progressBar.set_values(messages.copying_DLLs, 50)
            if self.game_config_form.qtObj.game_name_lineEdit.text() == "":
                self.progressBar.close()
                utilities.show_message_window("error", "ERROR", messages.missing_game_name)
                return

            if not self.game_config_form.qtObj.opengl_radioButton.isChecked() \
                and not self.game_config_form.qtObj.dx9_radioButton.isChecked() \
                and not self.game_config_form.qtObj.dx_radioButton.isChecked():
                self.progressBar.close()
                utilities.show_message_window("error", "ERROR", messages.missing_api)
                return

            games_obj = utilities.Object()
            games_obj.game_name = self.game_config_form.qtObj.game_name_lineEdit.text()

            if architecture == "32bits":
                games_obj.architecture = "32bits"
                src_path = constants.RESHADE32_PATH
            else:
                games_obj.architecture = "64bits"
                src_path = constants.RESHADE64_PATH

            games_sql = GamesSql(self)
            if self.selected_game is not None:
                if self.game_config_form.qtObj.dx9_radioButton.isChecked():
                    games_obj.api = "DX9"
                    dst_path = os.path.join(self.selected_game.game_dir, constants.D3D9)
                elif self.game_config_form.qtObj.dx_radioButton.isChecked():
                    games_obj.api = "DX11"
                    dst_path = os.path.join(self.selected_game.game_dir, constants.DXGI)
                else:
                    games_obj.api = "OPENGL"
                    dst_path = os.path.join(self.selected_game.game_dir, constants.OPENGL)

                if self.selected_game.name != games_obj.game_name or (self.selected_game.api != games_obj.api):
                    # checking name changes
                    # create Reshade.ini to replace edit CurrentPresetPath
                    old_screenshots_path = _get_screenshot_path(self, self.selected_game.game_dir, self.selected_game.name)
                    if len(old_screenshots_path) > 0:
                        t_path = "\\".join(old_screenshots_path.split("\\")[:-1])
                        new_screenshots_path = f"{t_path}\\{games_obj.game_name}"
                    else:
                        new_screenshots_path = ""

                    try:
                        dst_res_ini_path = os.path.join(self.selected_game.game_dir, constants.RESHADE_INI)
                        create_files = CreateFiles(self)
                        create_files.create_reshade_ini_file(dst_res_ini_path, new_screenshots_path)
                    except Exception as e:
                        self.log.error(f"create_reshade_ini_file: {str(e)}")

                    try:
                        # rename screenshot folder
                        if os.path.isdir(old_screenshots_path):
                            os.rename(old_screenshots_path, f"{new_screenshots_path}")
                    except OSError as e:
                        self.log.error(f"rename_screenshot_dir: {str(e)}")

                    try:
                        # deleting Reshade.dll
                        if self.selected_game.api.lower() == "opengl":
                            opengl_game_path = os.path.join(self.selected_game.game_dir, constants.OPENGL)
                            if os.path.isfile(opengl_game_path):
                                os.remove(opengl_game_path)
                        elif self.selected_game.api.lower() == "dx9":
                            d3d9_game_path = os.path.join(self.selected_game.game_dir, constants.D3D9)
                            if os.path.isfile(d3d9_game_path):
                                os.remove(d3d9_game_path)
                        else:
                            dxgi_game_path = os.path.join(self.selected_game.game_dir, constants.DXGI)
                            if os.path.isfile(dxgi_game_path):
                                os.remove(dxgi_game_path)
                    except OSError as e:
                        self.log.error(f"remove_reshade_file: {str(e)}")

                    try:
                        # creating Reshade.dll
                        shutil.copyfile(src_path, dst_path)
                    except shutil.Error as e:
                        self.log.error(f"copyfile: {src_path} to {dst_path} - {str(e)}")

                    utilities.show_message_window("info", "SUCCESS", f"{messages.game_updated}\n\n"
                                                                     f"{games_obj.game_name}")

                games_obj.id = self.selected_game.id
                games_sql.update_game(games_obj)
                self.progressBar.close()
            else:
                # new game added
                if self.game_config_form.qtObj.dx9_radioButton.isChecked():
                    games_obj.api = "DirectX 9"
                elif self.game_config_form.qtObj.opengl_radioButton.isChecked():
                    games_obj.api = "OpenGL"
                else:
                    games_obj.api = "DirectX 10/11/12"

                games_obj.path = self.added_game_path
                games_sql.insert_game(games_obj)
                del self.added_game_path
                _download_shaders(self)
                self.progressBar.close()
                _apply_single(self, games_obj)
                utilities.show_message_window("info", "SUCCESS", f"{messages.game_added}\n\n{games_obj.game_name}")

            self.populate_datagrid()
            self.game_config_form.close()
            self.enable_widgets(False)
        else:
            self.game_config_form.close()


def _get_screenshot_path(self, game_path, game_name):
    game_screenshots_path = ""
    # creating screenshot dir
    if self.qtobj.yes_screenshots_folder_radioButton.isChecked():
        game_screenshots_path = f"{constants.RESHADE_SCREENSHOT_PATH}\\{game_name}"
        try:
            if not os.path.exists(constants.RESHADE_SCREENSHOT_PATH):
                os.makedirs(constants.RESHADE_SCREENSHOT_PATH)
        except OSError as e:
            self.log.error(f"mkdir: {constants.RESHADE_SCREENSHOT_PATH} {str(e)}")

        try:
            if not os.path.exists(game_screenshots_path):
                os.makedirs(game_screenshots_path)
        except OSError as e:
            self.log.error(f"mkdir: {game_screenshots_path} {str(e)}")
    else:
        file = f"{game_path}\\{constants.RESHADE_INI}"
        reshade_config_screenshot_path = utilities.get_ini_settings(file, "GENERAL", "ScreenshotPath")
        if reshade_config_screenshot_path is not None:
            game_screenshots_path = reshade_config_screenshot_path
        elif os.path.isdir(f"{constants.RESHADE_SCREENSHOT_PATH}{game_name}"):
            game_screenshots_path = f"{constants.RESHADE_SCREENSHOT_PATH}{game_name}"

    return game_screenshots_path


def _apply_single(self, games_obj):
    errors = None
    game_path = "\\".join(games_obj.path.split("\\")[:-1])
    game_name = games_obj.game_name
    dst_res_ini_path = f"{game_path}\\{constants.RESHADE_INI}"
    dst_res_plug_ini_path = f"{game_path}\\{constants.RESHADE_PRESET_INI}"
    game_screenshots_path = _get_screenshot_path(self, game_path, game_name)

    if games_obj.architecture.lower() == "32bits":
        src_dll_path = constants.RESHADE32_PATH
    else:
        src_dll_path = constants.RESHADE64_PATH

    if games_obj.api.lower() == "dx9":
        dst_dll_path = f"{game_path}\\{constants.D3D9}"
    elif games_obj.api.lower() == "opengl":
        dst_dll_path = f"{game_path}\\{constants.OPENGL}"
    else:
        dst_dll_path = f"{game_path}\\{constants.DXGI}"

    try:
        try:
            # copying Reshade.dll
            shutil.copyfile(src_dll_path, dst_dll_path)
        except shutil.Error as e:
            self.log.error(f"copyfile: {str(e)}")

        create_files = CreateFiles(self)
        if self.reset_reshade_files:
            try:
                # create Reshade.ini for each game, because each game has different paths
                create_files.create_reshade_ini_file(dst_res_ini_path, game_screenshots_path)
            except Exception as e:
                self.log.error(f"create_reshade_ini_file: {str(e)}")

            try:
                # create ReShadePreset.ini inside program dir, then copy to game path
                create_files.create_reshade_preset_ini_file()
                shutil.copyfile(constants.RESHADE_PRESET_FILENAME, dst_res_plug_ini_path)
            except shutil.Error as e:
                self.log.error(f"create_reshade_preset_ini_file: {str(e)}")

            try:
                # create style.qss nside program dir
                create_files.create_style_file()
            except shutil.Error as e:
                self.log.error(f"create_style_file: {str(e)}")
        else:
            if not os.path.exists(dst_res_ini_path):
                try:
                    create_files.create_reshade_ini_file(dst_res_ini_path, game_screenshots_path)
                except Exception as e:
                    self.log.error(f"create_reshade_ini_file: {str(e)}")

            if not os.path.exists(constants.RESHADE_PRESET_FILENAME):
                try:
                    create_files.create_reshade_preset_ini_file()
                    shutil.copyfile(constants.RESHADE_PRESET_FILENAME, dst_res_plug_ini_path)
                except shutil.Error as e:
                    self.log.error(f"create_reshade_preset_ini_file: {str(e)}")
            else:
                shutil.copyfile(constants.RESHADE_PRESET_FILENAME, dst_res_plug_ini_path)

            if not os.path.exists(constants.STYLE_QSS_FILENAME):
                try:
                    create_files.create_style_file()
                except shutil.Error as e:
                    self.log.error(f"create_style_file: {str(e)}")
    except OSError as e:
        self.log.error(f"apply:[{game_name}:][{e.strerror.lower()}]")
        errors = f"- {game_name}: {e.strerror.lower()}"

    return errors


def _download_shaders(self):
    downloaded_new_shaders = None
    if not os.path.exists(constants.SHADERS_SRC_PATH) or (
            self.update_shaders is not None and self.update_shaders is True):
        downloaded_new_shaders = True
    elif self.update_shaders is not None and self.update_shaders is False:
        downloaded_new_shaders = False

    if downloaded_new_shaders is not None and downloaded_new_shaders is True:
        try:
            self.progressBar.set_values(messages.downloading_shaders, 50)
            r = requests.get(constants.SHADERS_ZIP_URL)
            with open(constants.SHADERS_ZIP_PATH, "wb") as outfile:
                outfile.write(r.content)
        except Exception as e:
            self.log.error(f"{messages.dl_new_shaders_timeout} {str(e)}")
            utilities.show_message_window("error", "ERROR", messages.dl_new_shaders_timeout)

        try:
            if os.path.exists(constants.SHADERS_SRC_PATH):
                shutil.rmtree(constants.SHADERS_SRC_PATH)
        except OSError as e:
            self.log.error(f"rmtree: {str(e)}")

        try:
            if os.path.exists(constants.RES_SHAD_MPATH):
                shutil.rmtree(constants.RES_SHAD_MPATH)
        except OSError as e:
            self.log.error(f"rmtree: {str(e)}")

        self.progressBar.set_values(messages.downloading_shaders, 75)
        if os.path.exists(constants.SHADERS_ZIP_PATH):
            try:
                utilities.unzip_file(constants.SHADERS_ZIP_PATH, constants.PROGRAM_PATH)
            except FileNotFoundError as e:
                self.log.error(str(e))
            except zipfile.BadZipFile as e:
                self.log.error(str(e))

            try:
                os.remove(constants.SHADERS_ZIP_PATH)
            except OSError as e:
                self.log.error(f"remove_file: {str(e)}")

        try:
            if os.path.exists(constants.RES_SHAD_MPATH):
                out_dir = f"{constants.PROGRAM_PATH}\\{constants.RESHADE_SHADERS}"
                os.rename(constants.RES_SHAD_MPATH, out_dir)
        except OSError as e:
            self.log.error(f"rename_path: {str(e)}")

        self.progressBar.set_values(messages.downloading_shaders, 99)
