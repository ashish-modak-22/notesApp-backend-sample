from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserRegister, UserResponse
from app.models.user import User
from fastapi import HTTPException
from app.core.security import hash_password



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
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    hashed_password = hash_password(user.password)

    new_user = User(
        name = user.name,
        email = user.email,
        password_hash = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
