# -*- coding: utf-8 -*-
import sqlalchemy as sa
from ddcDatabases import DBUtils
from ddcDatabases.exceptions import DBFetchAllException, DBFetchValueException
from sqlalchemy.sql import asc, collate
from src.database.models.games_model import Games


class GamesDal:
    def __init__(self, db_session, log):
        self.log = log
        self.columns = [x for x in Games.__table__.columns]
        self.db_utils = DBUtils(db_session)

    def insert_game(self, games_dict: dict):
        stmt = Games(
            name=games_dict["name"],
            architecture=games_dict["architecture"],
            api=games_dict["api"],
            dll=games_dict["dll"],
            path=games_dict["path"],
        )
        self.db_utils.insert(stmt)

    def update_game_path(self, game_id: int, new_game_path: str):
        stmt = sa.update(Games).where(Games.id == game_id).values(path=new_game_path)
        self.db_utils.execute(stmt)

    def update_game_architecture(self, game_id: int, new_game_architecture: str):
        stmt = sa.update(Games).where(Games.id == game_id).values(architecture=new_game_architecture)
        self.db_utils.execute(stmt)

    def update_game_api(self, game_id: int, new_game_api: str):
        stmt = sa.update(Games).where(Games.id == game_id).values(api=new_game_api)
        self.db_utils.execute(stmt)

    def delete_game(self, game_id: int):
        stmt = sa.delete(Games).where(Games.id == game_id)
        self.db_utils.execute(stmt)

    def get_all_games(self):
        try:
            stmt = sa.select(*self.columns).order_by(asc(collate(Games.name, "NOCASE")))
            results = self.db_utils.fetchall(stmt)
            return results
        except DBFetchAllException:
            return None

    def get_game_by_id(self, game_id: int):
        try:
            stmt = sa.select(*self.columns).where(Games.id == game_id)
            results = self.db_utils.fetchall(stmt)
            return results[0] if results else None
        except DBFetchValueException:
            return None

    def get_game_by_path(self, game_path: str):
        try:
            stmt = sa.select(*self.columns).where(Games.path == game_path)
            results = self.db_utils.fetchall(stmt)
            return results[0] if results else None
        except DBFetchValueException:
            return None

    def get_game_by_name(self, game_name: str):
        try:
            stmt = sa.select(*self.columns).where(Games.name == game_name)
            results = self.db_utils.fetchall(stmt)
            return results[0] if results else None
        except DBFetchValueException:
            return None

    def get_game_by_name_and_path(self, game_name: str, game_path: str):
        try:
            stmt = sa.select(*self.columns).where(Games.name == game_name, Games.path == game_path)
            results = self.db_utils.fetchall(stmt)
            return results[0] if results else None
        except DBFetchValueException:
            return None

    def update_game(self, games_dict: dict):
        stmt = (
            sa.update(Games)
            .where(Games.id == games_dict["id"])
            .values(
                name=games_dict["name"],
                api=games_dict["api"],
                dll=games_dict["dll"],
            )
        )
        self.db_utils.execute(stmt)
