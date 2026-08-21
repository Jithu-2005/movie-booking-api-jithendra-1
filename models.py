from pydantic import BaseModel


class Movie(BaseModel):
    Movie_name: str
    Theatre_name: str
    Ticket_price: int
    description: str

