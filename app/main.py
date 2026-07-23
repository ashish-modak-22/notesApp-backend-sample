from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserRegister, UserResponse
from app.models.user import User
from fastapi import HTTPException
from app.core.security import hash_password
from app.routers import auth



app  = FastAPI()


app.include_router(auth.router)


# Root endpoint that is called when the base URL ("/") is accessed
@app.get("/")
def home():

    # Return a welcome message in JSON format
    return {
        "message": "Welcome to NotesApp Backend"
    }


