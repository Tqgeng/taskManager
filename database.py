# настройка подключения к бд

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL = 'postgresql://postgres:123@localhost:5433/taskManagerProject'
# DATABASE_URL = 'postgresql://postgres:123@pg:5433/taskManagerProject'
DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()