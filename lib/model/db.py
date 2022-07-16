from __future__ import annotations
from sqlite3 import connect

import logging

log = logging.getLogger(__name__)


class Database():
    __slots__ = ("db_path", "sql_path", "calls", "db", "cur")

    def __init__(self, db_path, build_path) -> None:
        self.db_path = db_path
        self.sql_path = build_path
        self.calls = 0

    def connect(self) -> None:
        self.db = connect(self.db_path, check_same_thread=False)
        self.cur = self.db.cursor()
        log.info(f"Connected to database at {self.db_path}\n")

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.commit()
        self.db.close()
        log.info("Closed database connection")

    def record(self, command, *values):
        self.cur.execute(command, tuple(values))

        return self.cur.fetchone()

    def records(self, command, *values):
        self.cur.execute(command, tuple(values))

        return self.cur.fetchall()

    def field(self, command, *values):
        self.cur.execute(command, tuple(values))

        if (fetch := self.cur.fetchone()) is not None:
            return fetch[0]

    def execute(self, command, *values):
        self.cur.execute(command, tuple(values))

    def column(self, command, *values):
        self.cur.execute(command, tuple(values))

        return [item[0] for item in self.cur.fetchall()]

    def scriptexec(self, path):
        with open(path, 'r', encoding="utf-8") as script:
            self.cur.executescript(script.read())


# if __name__ == "__main__":
#     DB_PATH = "./lib/database/test.db"
#     BUILD_PATH = "./lib/schema/schema.sql"
#     db = Database(DB_PATH, BUILD_PATH)
#     db.connect()
