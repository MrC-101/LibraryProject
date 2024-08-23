import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import os
from dotenv import load_dotenv


def vacuum_analyze():
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = sqlalchemy.create_engine(DATABASE_URL)
    autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")
    with Session(autocommit_engine) as session:
        session.execute(text(f"VACUUM ANALYZE;"))
    session.close()
    engine.dispose()
    info = "ANALYZE Vacuum Completed Successfuly"
    length = max(len(info), len(DATABASE_URL))
    print("\n" + "=" * length)
    print(DATABASE_URL)
    print(info)
    print("=" * length + "\n")


def vacuum_full():
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = sqlalchemy.create_engine(DATABASE_URL)
    autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")
    with Session(autocommit_engine) as session:
        session.execute(text(f"VACUUM FULL;"))
    session.close()
    engine.dispose()
    info = "FULL Vacuum Completed Successfuly"
    length = max(len(info), len(DATABASE_URL))
    print("\n" + "=" * length)
    print(DATABASE_URL)
    print(info)
    print("=" * length + "\n")


def vacuum():
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = sqlalchemy.create_engine(DATABASE_URL)
    autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")
    with Session(autocommit_engine) as session:
        session.execute(text(f"VACUUM;"))
    session.close()
    engine.dispose()
    info = "Vacuum Completed Successfuly"
    length = max(len(info), len(DATABASE_URL))
    print("\n" + "=" * length)
    print(DATABASE_URL)
    print(info)
    print("=" * length + "\n")
