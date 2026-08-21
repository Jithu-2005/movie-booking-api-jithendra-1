from fastapi import FastAPI
from models import Movie
from database import engine, SessionLocal
import schemas
from schemas import movie
from typing import List



app = FastAPI()
schemas.Base.metadata.create_all(bind=engine)




@app.post("/movies")
def add_Movie(X:Movie):
    db = SessionLocal()
    new_Movie = schemas.movie(
        Movie_name = X.Movie_name,
        Theatre_name = X.Theatre_name,
        Ticket_price = X.Ticket_price,
        description = X.description
    )
    db.add(new_Movie)
    db.commit()
    return {"Movie Added Successfully"}
    
    

@app.get("/movies", response_model=List[Movie])
def get_all_Movies():
    db = SessionLocal()
    try:
        all_movies = db.query(schemas.movie).all()
        return all_movies
    finally:
        db.close()

# @app.get("/product/{Movie_name}")
# def get_product_by_Movie_name(Movie_name:str):
#     for product in products:
#         if product.Movie_name == Movie_name:
#             return product
#     if product.Movie_name not in products:
#         raise HTTPException(status_code=404, detail="Movie not found")