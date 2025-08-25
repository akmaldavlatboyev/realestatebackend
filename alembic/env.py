import sys, os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# sys.path to'g'irlash
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db.session import engine
from app.db.base import Base
from app.models import user, otp   # barcha modellaring import qilinsin

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=str(engine.url),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
