from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String




Base = declarative_base()

class movie(Base):
    __tablename__ = "Movie_Details"

    Movie_name = Column(String, index = True)
    Theatre_name = Column(String, primary_key=True,index = True)
    Ticket_price = Column(Integer, index = True)
    description = Column(String, index = True)