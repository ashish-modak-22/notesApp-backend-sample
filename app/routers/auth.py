from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserResponse, UserLogin
from app.core.security import hash_password, verify_password, create_access_token



router = APIRouter(
    prefix = "/auth",
    tags = ["Authentication"]    
)


@router.post("/register", response_model=UserResponse)
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



@router.post("/login")
async def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    
    existing_user = db.query(User).filter(
    User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(user.password, existing_user.password_hash):
        raise HTTPException(
            status_code=404,
            detail="Invalid email or password"
        )

    # Create a JWT access token for the authenticated user
    access_token = create_access_token(
        data={
            "sub": existing_user.email
        }
    )
    
    return {
        "message": "Login Successful",
        "user_id": existing_user.id,
        "name": existing_user.name,
        "email": existing_user.email
    }