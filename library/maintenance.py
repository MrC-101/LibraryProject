import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import os
from flask import flash
from dotenv import load_dotenv


def vacuum_analyze():
    load_dotenv()
    DATABASE_URL = os.getenv('DATABASE_URL')
    engine = sqlalchemy.create_engine(DATABASE_URL)
    autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")
    with Session(autocommit_engine) as session:
        session.execute(text(f'VACUUM ANALYZE;'))
    session.close()
    engine.dispose()
    print('\n'+'=' * 50)
    print(DATABASE_URL)
    print('ANALYZE Vacuum Completed Successfuly')
    print('=' * 50+'\n')

def vacuum_full():
    load_dotenv()
    DATABASE_URL = os.getenv('DATABASE_URL')
    engine = sqlalchemy.create_engine(DATABASE_URL)
    autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")
    with Session(autocommit_engine) as session:
        session.execute(text(f'VACUUM FULL;'))
    session.close()
    engine.dispose()
    print('\n'+'=' * 50)
    print(DATABASE_URL)
    print('FULL Vacuum Completed Successfuly')
    print('=' * 50+'\n')
    
def vacuum():
    load_dotenv()
    DATABASE_URL = os.getenv('DATABASE_URL')
    engine = sqlalchemy.create_engine(DATABASE_URL)
    autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")
    with Session(autocommit_engine) as session:
        session.execute(text(f'VACUUM;'))
    session.close()
    engine.dispose()
    print('\n'+'=' * 50)
    print(DATABASE_URL)
    print('Vacuum Completed Successfuly')
    print('=' * 50+'\n')