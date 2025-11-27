
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# MySQL credentials
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
# Use the DB name requested: "DAQ project"
# Note: spaces are allowed in MySQL DB names when quoted, but the
# SQLAlchemy URL cannot contain raw spaces — encode for the URL path.
MYSQL_DB = os.getenv('MYSQL_DB', 'DAQ project')

# 1. Connect to MySQL server (no DB) and create DB if not exists
SERVER_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/"
engine_tmp = create_engine(SERVER_URL, pool_pre_ping=True)
def ensure_database_exists(retries: int = 1):
	"""Ensure the target MySQL database exists by connecting to the server
	(without selecting a database) and issuing a CREATE DATABASE IF NOT EXISTS.

	This function creates and disposes a short-lived engine so importing the
	module does not attempt a network call. Call this from an application
	startup hook so the app can start even when the DB is temporarily down.
	"""
	engine_tmp_local = create_engine(SERVER_URL, pool_pre_ping=True)
	try:
		with engine_tmp_local.connect() as conn:
			conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DB}`"))
			conn.commit()
	finally:
		engine_tmp_local.dispose()

# 2. Now connect to the target DB
# Build the SQLAlchemy URL using the URL object so the database name is sent as
# a separate parameter (this preserves spaces and special characters) instead of
# being embedded (and percent-encoded) in the path portion of a raw URL string.
SQLALCHEMY_DATABASE_URL = URL.create(
	drivername="mysql+mysqlconnector",
	username=MYSQL_USER,
	password=MYSQL_PASSWORD,
	host=MYSQL_HOST,
	port=int(MYSQL_PORT) if MYSQL_PORT.isdigit() else MYSQL_PORT,
	database=MYSQL_DB,
)
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
