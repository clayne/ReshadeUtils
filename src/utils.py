# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-


import os
import sys
import json
import zipfile
import requests
import datetime
import configparser
from src.files import Files
from src.sql.config_sql import ConfigSql
from src import constants, messages, qtutils


class Object:
    def __init__(self):
        self._created = datetime.datetime.now().isoformat()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_dict(self):
        json_string = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        json_dict = json.loads(json_string)
        return json_dict


# def get_current_path():
#     path = os.path.abspath(os.getcwd())
#     if path is not None:
#         return os.path.normpath(path)
#     return None


def get_ini_settings(file_name, section, config_name):
    parser = configparser.ConfigParser(delimiters="=", allow_no_value=True)
    parser.optionxform = str  # this wont change all values to lowercase
    parser._interpolation = configparser.ExtendedInterpolation()
    parser.read(file_name)
    try:
        value = parser.get(section, config_name).replace("\"", "")
    except Exception:
        value = None
    if value is not None and len(value) == 0:
        value = None
    return value


def unzip_reshade(self, local_reshade_exe):
    try:
        if os.path.isfile(constants.RESHADE32_PATH):
            os.remove(constants.RESHADE32_PATH)
        if os.path.isfile(constants.RESHADE64_PATH):
            os.remove(constants.RESHADE64_PATH)
        unzip_file(local_reshade_exe, constants.PROGRAM_PATH)
    except Exception as e:
        self.log.error(str(e))


def unzip_file(file_name, out_path):
    zipfile_path = file_name
    zipf = zipfile.ZipFile(zipfile_path)
    zipf.extractall(out_path)
    zipf.close()


# def get_download_path():
#     if constants.IS_WINDOWS:
#         import winreg
#         sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
#         downloads_guid = "{374DE290-123F-4565-9164-39C4925E467B}"
#         with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
#             downloads_path = winreg.QueryValueEx(key, downloads_guid)[0]
#         return downloads_path
#     else:
#         t1_path = str(os.path.expanduser("~/Downloads"))
#         t2_path = f"{t1_path}".split("\\")
#         downloads_path = "/".join(t2_path)
#         return downloads_path.replace("\\", "/")


def get_pictures_path():
    if os.name == "nt":
        import winreg
        sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        pictures_guid = "My Pictures"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            pictures_path = winreg.QueryValueEx(key, pictures_guid)[0]
        return pictures_path
    else:
        pictures_path = os.path.normpath(os.path.expanduser("~/Pictures"))
        return pictures_path


def check_new_program_version(self):
    client_version = self.client_version
    remote_version = None
    remote_version_filename = constants.REMOTE_VERSION_FILENAME
    obj_return = Object()
    obj_return.new_version_available = False
    obj_return.new_version = None

    try:
        req = requests.get(remote_version_filename, stream=True)
        if req.status_code == 200:
            for line in req.iter_lines(decode_unicode=True):
                if line:
                    remote_version = line.rstrip()
                    break

            if remote_version is not None and (float(remote_version) > float(client_version)):
                obj_return.new_version_available = True
                obj_return.new_version_msg = f"Version {remote_version} available for download"
                obj_return.new_version = float(remote_version)
        else:
            err_msg = f"{messages.error_check_new_version}\n{messages.remote_version_file_not_found}\ncode: {req.status_code}"
            qtutils.show_message_window(self.log, "error", err_msg)
    except requests.exceptions.ConnectionError:
        qtutils.show_message_window(self.log, "error", messages.dl_new_version_timeout)

    return obj_return


def check_dirs():
    try:
        if not os.path.isdir(constants.PROGRAM_PATH):
            os.makedirs(constants.PROGRAM_PATH)
    except OSError as e:
        err_msg = f"{messages.unable_create_dirs}\n{e}"
        qtutils.show_message_window(None, "error", err_msg)
        exit(1)


def create_local_reshade_files(self):
    files = Files(self)

    try:
        if not os.path.isfile(constants.RESHADE_INI_FILENAME):
            files.download_reshade_ini_file()
    except Exception as e:
        err_msg = f"{str(e)}\n\n{constants.RESHADE_INI_FILENAME}{messages.not_found}"
        qtutils.show_message_window(self.log, "error", err_msg)
        return False

    try:
        if not os.path.isfile(constants.RESHADE_PRESET_FILENAME):
            files.download_reshade_preset_file()
    except Exception as e:
        err_msg = f"{str(e)}\n\n{constants.RESHADE_PRESET_FILENAME}{messages.not_found}"
        qtutils.show_message_window(self.log, "error", err_msg)
        return False

    try:
        if not os.path.isfile(constants.QSS_FILENAME):
            files.download_qss_file()
    except Exception as e:
        err_msg = f"{str(e)}\n\n{constants.QSS_FILENAME}{messages.not_found}"
        qtutils.show_message_window(self.log, "error", err_msg)
        return False

    return True


def check_db_connection(self):
    if self.database is not None:
        conn = self.database.engine.connect()
        if conn is not None:
            conn.close()
            return True
    err_msg = f"{messages.error_db_connection}\n\n{messages.exit_program}"
    if qtutils.show_message_window(self.log, "error", err_msg):
        sys.exit(1)


def check_database_configs(self):
    if not create_default_tables(self):
        err_msg = f"{messages.error_db_connection}\n\n{messages.exit_program}"
        if qtutils.show_message_window(self.log, "error", err_msg):
            sys.exit(1)

    config_sql = ConfigSql(self)
    rs_config = config_sql.get_program_version()
    if rs_config is not None:
        program_version = rs_config[0].get("program_version")
        if float(program_version) < float(constants.RESET_DATABASE_VERSION):
            try:
                os.remove(constants.SQLITE3_FILENAME)
                check_db_connection(self)
                qtutils.show_message_window(self.log, "warning", messages.config_reset_msg)
            except Exception:
                err_msg = f"{messages.error_db_connection}\n\n{messages.exit_program}"
                if qtutils.show_message_window(self.log, "error", err_msg):
                    sys.exit(1)

    if not set_default_database_configs(self, constants.VERSION):
        err_msg = f"{messages.error_create_sql_config_msg}\n\n{messages.exit_program}"
        if qtutils.show_message_window(self.log, "error", err_msg):
            sys.exit(1)


def create_default_tables(self):
    from src.sql.tables import Configs, Games
    try:
        Configs.__table__.create(self.database.engine, checkfirst=True)
        Games.__table__.create(self.database.engine, checkfirst=True)
    except Exception as e:
        self.log.error(str(e))
        return False
    return True


def set_default_database_configs(self, program_version):
    from src.sql.config_sql import ConfigSql
    config_sql = ConfigSql(self)
    rs_config = config_sql.get_program_version()
    if rs_config is None and not config_sql.set_default_configs():
        return False
    config_sql.update_program_version(program_version)
    return True


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./src")
    return os.path.join(base_path, relative_path)


def check_game_file(self):
    if self.selected_game is not None:
        if not os.path.isfile(self.selected_game.path):
            return False
    else:
        if not os.path.isfile(self.added_game_path):
            return False
    return True


def set_file_settings(filename: str, section: str, config_name: str, value):
    parser = configparser.ConfigParser(delimiters="=", allow_no_value=False)
    parser.optionxform = str  # this wont change all values to lowercase
    parser._interpolation = configparser.ExtendedInterpolation()
    parser.read(filename)
    parser.set(section, config_name, value)
    try:
        with open(filename, "w") as configfile:
            parser.write(configfile, space_around_delimiters=False)
    except configparser.DuplicateOptionError:
        return


def get_binary_type(self, game_path):
    import struct

    image_file_machine_i386 = 332
    image_file_machine_ia64 = 512
    image_file_machine_amd64 = 34404
    image_file_machine_arm = 452
    image_file_machine_aarch64 = 43620

    with open(game_path, "rb") as f:
        s = f.read(2)
        if s != b"MZ":
            self.log.info("Not an EXE file")
            return None
        else:
            f.seek(60)
            s = f.read(4)
            header_offset = struct.unpack("<L", s)[0]
            f.seek(header_offset+4)
            s = f.read(2)
            machine = struct.unpack("<H", s)[0]

            if machine == image_file_machine_i386:
                # self.log.info("IA32 (32-bit x86)")
                return "IA32"
            elif machine == image_file_machine_ia64:
                # self.log.info("IA64 (Itanium)")
                return "IA64"
            elif machine == image_file_machine_amd64:
                # self.log.info("AMD64 (64-bit x86)")
                return "AMD64"
            elif machine == image_file_machine_arm:
                # self.log.info("ARM eabi (32-bit)")
                return "ARM-32bits"
            elif machine == image_file_machine_aarch64:
                # self.log.info("AArch64 (ARM-64, 64-bit)")
                return "ARM-64bits"
            else:
                # self.log.info(f"Unknown architecture {machine}")
                return None