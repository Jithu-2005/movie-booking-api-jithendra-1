from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String, ForeignKey




Base = declarative_base()

class movie(Base):
    __tablename__ = "Movie_Details"
    id = Column(Integer, primary_key=True, index = True, autoincrement = True)

    Movie_name = Column(String, index = True)
    Theatre_name = Column(String, index = True)
    Ticket_price = Column(Integer, index = True)
    description = Column(String, index = True)
    #Add ID and Seat Tracking to the Database
    language = Column(String, index = True, default = "Telugu")
    total_seats = Column(Integer, default = 100)
    available_seats = Column(Integer, default = 100)


    class booking(Base):
        __tablename__ = "Booking_Details"
        id = Column(Integer, primary_key = True, index = True, autoincrement = True)
        movie_id = Column(Integer, ForeignKey("Movie_Details.id"))
        seats_booked = Column(Integer)
        total_amount = Column(Integer)
    