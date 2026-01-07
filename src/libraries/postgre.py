"""
pgpool.py
Simple PostgreSQL helper with connection pooling and basic CRUD.
"""

from os import getenv as env
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import atexit


class PostgresPool:
    def __init__(
        self,
        *,
        host: str,
        port: int = 5432,
        database: str,
        user: str,
        password: str,
        minconn: int = 1,
        maxconn: int = 10,
    ):
        self._pool = pool.SimpleConnectionPool(
            minconn,
            maxconn,
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )

        if not self._pool:
            raise RuntimeError("Failed to create PostgreSQL connection pool")

        # Ensure cleanup on normal interpreter shutdown
        atexit.register(self.close_all)

    # ---------------------------
    # Internal helpers
    # ---------------------------
    def _get_conn(self):
        return self._pool.getconn()

    def _put_conn(self, conn):
        self._pool.putconn(conn)

    # ---------------------------
    # CRUD operations
    # ---------------------------
    def fetch_one(self, query: str, params: tuple | None = None) -> dict | None:
        conn = self._get_conn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                return cur.fetchone()
        finally:
            self._put_conn(conn)

    def fetch_all(self, query: str, params: tuple | None = None) -> list[dict]:
        conn = self._get_conn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                return cur.fetchall()
        finally:
            self._put_conn(conn)

    def insert(self, query: str, params: tuple | None = None) -> int | None:
        """
        Returns last inserted id if RETURNING is used, else None.
        """
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
                if cur.description:
                    return cur.fetchone()[0]
                return None
        except Exception:
            conn.rollback()
            raise
        finally:
            self._put_conn(conn)

    def update(self, query: str, params: tuple | None = None) -> int:
        """
        Returns number of rows affected.
        """
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
                return cur.rowcount
        except Exception:
            conn.rollback()
            raise
        finally:
            self._put_conn(conn)

    def delete(self, query: str, params: tuple | None = None) -> int:
        """
        Returns number of rows deleted.
        """
        return self.update(query, params)

    # ---------------------------
    # Resource cleanup
    # ---------------------------
    def close_all(self):
        if self._pool:
            self._pool.closeall()
            self._pool = None


postgre = PostgresPool(
    host=env("DB_HOST"),
    port=int(env("DB_PORT")),
    user=env("DB_USER"),
    password=env("DB_PASSWORD"),
    database=env("DB_NAME"),
    maxconn=env("DB_MAX_CONNECTION") or 10,
)
