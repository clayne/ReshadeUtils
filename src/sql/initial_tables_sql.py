#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

from src.sql.sqlite3_connection import Sqlite3


class InitialTablesSql:
    def __init__(self, main):
        self.main = main
        self.log = main.log


    def create_initial_tables(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS configs (
            id                              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            use_dark_theme                  int(1)  NOT NULL DEFAULT 0,
            update_shaders                  int(1)  NOT NULL DEFAULT 1,
            check_program_updates           int(1)  NOT NULL DEFAULT 1,
            check_reshade_updates           int(1)  NOT NULL DEFAULT 1,
            silent_reshade_updates          int(1)  NOT NULL DEFAULT 1,
            reset_reshade_files             int(1)  NOT NULL DEFAULT 0,
            use_custom_config               int(1)  NOT NULL DEFAULT 0,
            create_screenshots_folder       int(1)  NOT NULL DEFAULT 1,
            program_version                 TEXT,
            reshade_version                 TEXT,
            CONSTRAINT  check_use_dark_theme CHECK (use_dark_theme IN (0,1)),
            CONSTRAINT  check_update_shaders CHECK (update_shaders IN (0,1)),
            CONSTRAINT  check_program_updates CHECK (check_program_updates IN (0,1)),
            CONSTRAINT  check_reshade_updates CHECK (check_reshade_updates IN (0,1)),
            CONSTRAINT  check_silent_reshade_updates CHECK (silent_reshade_updates IN (0,1)),
            CONSTRAINT  check_reset_reshade_files CHECK (reset_reshade_files IN (0,1)),
            CONSTRAINT  check_use_custom_config CHECK (use_custom_config IN (0,1)),
            CONSTRAINT  check_create_screenshots_folder CHECK (create_screenshots_folder IN (0,1))
        );
        
        CREATE TABLE IF NOT EXISTS games (
            id             INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            name           TEXT     NOT NULL,
            architecture   TEXT     NOT NULL,
            api            TEXT     NOT NULL,
            path           TEXT     NOT NULL
        );

        """
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)
