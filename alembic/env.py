import os, sys
from logging.config import fileConfig
from dotenv import load_dotenv

# add project root to path so `app` package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from alembic import context
from sqlalchemy import engine_from_config, pool

# this loads the alembic.ini config file
config = context.config
fileConfig(config.config_file_name)

# load .env so os.getenv can read DATABASE_URL
load_dotenv()
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# import Base and models so metadata is populated
from app.db.base import Base  # adjust path if Base elsewhere

# Force import models to register tables on Base.metadata
try:
    import app.models.project  # noqa: F401
    import app.models.task     # noqa: F401
except Exception:
    # if your models live in different modules, import those instead
    pass

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
