#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

import os
import sys
import requests
import subprocess
from PyQt6 import QtCore, QtWidgets
from src.sql.config_sql import ConfigSql
from src import constants, messages, utils, qtutils, log


class Launcher:
    def __init__(self):
        self.progressBar = qtutils.ProgressBar()
        self.log = None
        self.new_version = None
        self.new_version_msg = None
        self.client_version = None


    def init(self):
        self.progressBar.set_values(messages.checking_files, 25)
        utils.check_dirs()
        self.log = log.setup_logging(self)
        utils.check_files(self)

        self.progressBar.set_values(messages.checking_db_connection, 50)
        utils.check_db_connection(self)
        utils.set_default_database_configs(self)

        self.progressBar.set_values(messages.checking_new_version, 75)
        self._check_update_required()
        self.progressBar.close()
        self._call_program()


    def _check_update_required(self):
        config_sql = ConfigSql(self)
        rs_config = config_sql.get_configs()

        if rs_config[0].get("program_version") is None:
            self.client_version = constants.VERSION
        else:
            self.client_version = rs_config[0].get("program_version")

        if rs_config[0].get("check_program_updates"):
            new_version_obj = utils.check_new_program_version(self)
            if new_version_obj.new_version_available:
                self.new_version = new_version_obj.new_version
                self.new_version_msg = new_version_obj.new_version_msg
                self._download_new_program_version(False)


    def _download_new_program_version(self, show_dialog=True):
        if show_dialog:
            msg = f"""{messages.new_version_available}
                \nYour version: v{self.client_version}\nNew version: v{self.new_version}
                \n{messages.confirm_download}"""
            reply = qtutils.show_message_window("question", self.new_version_msg, msg)

            if reply == QtWidgets.QMessageBox.No:
                new_title = f"{constants.FULL_PROGRAM_NAME} ({self.new_version_msg})"
                _translate = QtCore.QCoreApplication.translate
                self.form.setWindowTitle(_translate("Main", new_title))
                return

        program_url = f"{constants.GITHUB_EXE_PROGRAM_URL}{self.new_version}/{constants.EXE_PROGRAM_NAME}"
        downloaded_program_path = f"{utils.get_current_path()}\\{constants.EXE_PROGRAM_NAME}"

        r = requests.get(program_url)
        if r.status_code == 200:
            with open(downloaded_program_path, "wb") as outfile:
                outfile.write(r.content)
            qtutils.show_message_window("Info", "INFO", f"{messages.program_updated}v{self.new_version}")
        else:
            qtutils.show_message_window("error", "ERROR", f"{messages.error_dl_new_version}")
            self.log.error(f"{messages.error_dl_new_version} {r.status_code} {r}")


    def _call_program(self):
        code = None
        cmd = [f"{os.path.abspath(os.getcwd())}\\{constants.EXE_PROGRAM_NAME}"]
        try:
            process = subprocess.run(cmd, shell=True, check=True, universal_newlines=True)
            #output = process.stdout
            code = process.returncode
        except Exception as e:
            emsg = None
            if code is None:
                code = e.returncode
                emsg = f"cmd:{cmd} - code:{code} - {e}"
            self.log.error(f"{messages.error_executing_program}{constants.EXE_PROGRAM_NAME}"
                           f" - {messages.error_check_installation} - {emsg}")
            qtutils.show_message_window("error", "ERROR",
                                          f"{messages.error_executing_program}{constants.EXE_PROGRAM_NAME}\n"
                                          f"{messages.error_check_installation}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    launcher = Launcher()
    launcher.init()
    sys.exit(0)
