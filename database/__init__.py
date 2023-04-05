import os, sys, sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

DB_URL = os.getenv("DATABASE_URL", "")
if DB_URL:
   print("Got DATABASE_URL")
   if 'postgres' in DB_URL and 'postgresql' not in DB_URL:
      DB_URL = DB_URL.replace("postgres", "postgresql")
else:
   print("You didn't fill DATABASE_URL")
   sys.exit()

def start() -> scoped_session:
    engine = sqlalchemy.create_engine(DB_URL, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()
