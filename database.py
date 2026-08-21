from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
URL_DATABASE='postgresql://postgres:Rama%402005@localhost:5432/Task' # database://username:pwd@localhost:portno/database_name

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)