from fastapi import FastAPI,HTTPException,Depends,status
from models import Movie, BookingCreate
from database import engine, SessionLocal
import schemas
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "my-super-secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials



app = FastAPI(dependencies=[Depends(verify_token)])
schemas.Base.metadata.create_all(bind=engine)


# Post the Movie


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
    

# Get all Movies
 

@app.get("/movies")
def get_all_Movies():
    db = SessionLocal()
    try:
        all_movies = db.query(schemas.movie).all()
        return all_movies
    finally:
        db.close()


#Get Movie by ID


@app.get("/movies/{movie_id}")
def get_movie_by_id(movie_id: int):
    db = SessionLocal()
    try:
        movie = db.query(schemas.movie).filter(schemas.movie.id == movie_id).first()
        if not movie:
            raise HTTPException(status_code = 404, detail = "Movie not found")
        return movie
    finally:
        db.close()


# Update movie details


@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, X: Movie):
    db = SessionLocal()
    try:
        movie = db.query(schemas.movie).filter(schemas.movie.id == movie_id).first()
        if not movie:
            raise HTTPException(status_code = 404, detail = "Movie not found")
        movie.Movie_name = X.Movie_name
        movie.Theatre_name = X.Theatre_name
        movie.Ticket_price = X.Ticket_price
        movie.description = X.description
        movie.language = X.language
        movie.total_seats = X.total_seats

        db.commit()
        return {"message": "Movie updated successfully"}
    finally:
        db.close()


# Remove


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    db = SessionLocal()
    try:
        movie = db.query(schemas.movie).filter(schemas.movie.id == movie_id).filter
        if not movie:
            raise HTTPException(status_code = 404, detail = "Movie not found")
        db.delete(movie)
        db.commit()
        return {"message": "Movie deleted successfully"}
    finally:
        db.close()


# Book tickets


@app.post("/bookings", status_code=201)
def book_tickets(booking_req: BookingCreate):
    db = SessionLocal()
    try:
        movie = db.query(schemas.movie).filter(schemas.movie.id == booking_req.movie_id).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        if movie.available_seats < booking_req.seats_to_book:
            raise HTTPException(status_code=400, detail="Not enough seats available")

        movie.available_seats -= booking_req.seats_to_book
        
        total_cost = movie.Ticket_price * booking_req.seats_to_book
        new_booking = schemas.booking(
            movie_id=movie.id,
            seats_booked=booking_req.seats_to_book,
            total_amount=total_cost
        )
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        
        return {"message": "Tickets booked successfully", "booking_id": new_booking.id, "total_amount": total_cost}
    finally:
        db.close()


# Get booking details


@app.get("/bookings/{booking_id}")
def get_booking(booking_id: int):
    db = SessionLocal()
    try:
        booking = db.query(schemas.booking).filter(schemas.booking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return booking
    finally:
        db.close()


# Cancel a booking


@app.delete("/bookings/{booking_id}")
def cancel_booking(booking_id: int):
    db = SessionLocal()
    try:
        booking = db.query(schemas.booking).filter(schemas.booking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        # Return seats to the movie
        movie = db.query(schemas.movie).filter(schemas.movie.id == booking.movie_id).first()
        if movie:
            movie.available_seats += booking.seats_booked
        
        db.delete(booking)
        db.commit()
        return {"message": "Booking cancelled successfully, seats returned."}
    finally:
        db.close()


#  Return seat counts


@app.get("/movies/{movie_id}/seats")
def get_movie_seats(movie_id: int):
    db = SessionLocal()
    try:
        movie = db.query(schemas.movie).filter(schemas.movie.id == movie_id).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        booked_seats = movie.total_seats - movie.available_seats
        return {
            "total_seats": movie.total_seats,
            "booked_seats": booked_seats,
            "available_seats": movie.available_seats
        }
    finally:
        db.close()


# Filter


@app.get("/movies/language/{language}")
def get_movies_by_language(language: str):
    db = SessionLocal()
    try:
        movies = db.query(schemas.movie).filter(schemas.movie.language.ilike(language)).all()
        return movies
    finally:
        db.close()