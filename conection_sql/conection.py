from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "mysql://cancunseadust_powerbi:BGgh5646hdd098undgdgDd!?@185.215.224.169/cancunseadust_DWHSurvey"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

# con = engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()