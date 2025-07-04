from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.db import Base
from app.models import user, product, order
from dotenv import load_dotenv

load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

DB_URL = os.getenv("DATABASE_URL")


def run_migrations_offline():
    if not DB_URL:
        print("[Alembic] Error: No database URL found. Please set the DATABASE_URL environment variable.")
        return
    context.configure(
        url=DB_URL, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    if not DB_URL:
        print("[Alembic] Error: No database URL found. Please set the DATABASE_URL environment variable.")
        return
    try:
        connectable = engine_from_config(
            {"sqlalchemy.url": DB_URL},
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=target_metadata, compare_type=True
            )
            with context.begin_transaction():
                context.run_migrations()
    except Exception as e:
        print(f"[Alembic] Database connection error: {e}\nCheck your DATABASE_URL and database server.")

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online() 