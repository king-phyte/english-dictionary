import sqlite3
from json import dumps, loads
from pathlib import Path
from sqlite3 import Connection
from typing import Any, Generator, Optional, Union

from .api import BaseAPI

DATABASE_DIRECTORY = Path(__file__).resolve().parent
DATABASE_NAME = "words.db"


class Database:
    """
    Supports using the class as a context manager, but commits and rollbacks are done automatically when this is used.

    When another approach is used (such as instantiation), commits and rollbacks should be done manually.

    The connection to the database is closed when
    the context manager is exited or all references to the instance of the database are deleted
    """

    def __init__(
        self,
        url: Union[Path, str] = (DATABASE_DIRECTORY / DATABASE_NAME),
    ) -> None:
        self._url = url
        self._connection: Optional[Connection] = None
        self.create_words_database_if_not_exist()

    def _connect(self) -> None:
        self._connection = sqlite3.connect(self._url)

    def get_connection(self) -> Connection:
        """Return a database connection"""
        if not self._connection:
            self._connect()
        return self._connection

    def close_connection(self) -> None:
        """Close the database connection"""
        if self._connection:
            self._connection.close()

    def __del__(self) -> None:
        """Close the database connection when there are no references to it"""
        self.close_connection()
        self._connection = None

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        if exc_traceback is None:
            self._connection.commit()
        else:
            self._connection.rollback()

        self.close_connection()

    def create_words_database_if_not_exist(self) -> None:
        with self.get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    data JSON
                )
                """
            )

    def fetch_all_words(self) -> Generator[Optional[BaseAPI], Any, None]:
        """Yield all word data (BaseAPI) found in the database, if any"""
        for row in self.get_connection().execute(
            """
            SELECT data FROM words
            """
        ):
            yield [
                loads(row[0]),
            ]

    def save_word(self, word_data: BaseAPI) -> None:
        """Save a word to the database"""
        word_data = word_data[0]
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO words (name, data)
                VALUES (?, ?)
                """,
                (
                    word_data["name"],
                    dumps(word_data),
                ),
            )

    def edit_word(self, word_data: BaseAPI) -> None:
        word_data = word_data[0]
        with self.get_connection() as conn:
            conn.execute(
                """
                UPDATE words
                SET data = ?
                WHERE name = ?
                """,
                (
                    dumps(word_data),
                    word_data["name"],
                ),
            )

    def delete_word(self, word: str) -> None:
        """Removes a word from database. Warning: Destructive action"""
        with self.get_connection() as conn:
            conn.execute(
                """
                DELETE FROM words WHERE name = (?)
                """,
                (word,),
            )
