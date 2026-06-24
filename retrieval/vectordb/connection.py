"""
Database connection module.
"""

import psycopg

from retrieval.config.settings import Settings


class DatabaseConnection:
    """Handles PostgreSQL database connection."""

    @staticmethod
    def connect():
        """
        Create and return a PostgreSQL connection.
        """

        try:
            return psycopg.connect(
                host=Settings.DB_HOST,
                port=Settings.DB_PORT,
                dbname=Settings.DB_NAME,
                user=Settings.DB_USER,
                password=Settings.DB_PASSWORD,
            )

        except psycopg.Error as error:
            raise ConnectionError(
                f"Failed to connect to PostgreSQL: {error}"
            ) from error