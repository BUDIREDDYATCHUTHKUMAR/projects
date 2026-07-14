import sys
import os

# 1. CRUCIAL: This MUST run first so Python knows where your 'app' folder sits!
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.database import Base
from logging.config import fileConfig
from app.models.users import User  # Ensure this path matches your exact user model name
from app.models.workspace import Workspace
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from app.core.config import settings
from alembic import context

# This is the Alembic Config object
config = context.config

# ==========================================
#  THE FIX: FORCE OVERRIDE DATABASE URL
# ==========================================
# This actively replaces the broken text inside alembic.ini with your real .env database link
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set up database table autogenerate support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Now this reads the valid URL we injected above instead of crashing on 'driver'
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
