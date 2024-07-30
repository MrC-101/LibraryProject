import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import os
from dotenv import load_dotenv

def vacuum():
    DATABASE_URL = os.getenv('DATABASE_URL')
    print(DATABASE_URL)
    engine = sqlalchemy.create_engine(DATABASE_URL)
    autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")
    with Session(autocommit_engine) as session:
        session.execute(text(f'VACUUM ANALYZE;'))
    session.close()
    engine.dispose()
    print('Vacuum Completed Successfuly')