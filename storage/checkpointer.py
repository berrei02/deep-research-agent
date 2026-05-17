from contextlib import contextmanager
from langgraph.checkpoint.postgres import PostgresSaver
import config


@contextmanager
def get_checkpointer(db_uri: str = config.DATABASE_URL):
    """Context manager that provides a ready PostgreSQL checkpointer."""
    with PostgresSaver.from_conn_string(db_uri) as saver:
        saver.setup()
        yield saver
