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
            connect_kwargs = {
                "host": Settings.DB_HOST,
                "port": Settings.DB_PORT,
                "dbname": Settings.DB_NAME,
                "user": Settings.DB_USER,
                "password": Settings.DB_PASSWORD,
            }
            optional_settings = {
                "sslmode": Settings.DB_SSLMODE,
                "sslrootcert": Settings.DB_SSLROOTCERT,
                "sslcert": Settings.DB_SSLCERT,
                "sslkey": Settings.DB_SSLKEY,
                "application_name": Settings.DB_APPLICATION_NAME,
                "connect_timeout": Settings.DB_CONNECT_TIMEOUT,
            }
            connect_kwargs.update(
                {key: value for key, value in optional_settings.items() if value}
            )

            return psycopg.connect(
                **connect_kwargs,
            )

        except psycopg.Error as error:
            raise ConnectionError(
                f"Failed to connect to PostgreSQL: {error}"
            ) from error
