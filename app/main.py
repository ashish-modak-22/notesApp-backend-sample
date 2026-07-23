from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserRegister, UserResponse


app  = FastAPI()


# Root endpoint that is called when the base URL ("/") is accessed
@app.get("/")
def home():

    # Return a welcome message in JSON format
    return {
        "message": "Welcome to NotesApp Backend"
    }


@app.post("/register", response_model=UserResponse)
async def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    pass