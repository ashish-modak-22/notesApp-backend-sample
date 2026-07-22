import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker




# Load the environment variables
load_dotenv()



# Read the database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")



# Create the PostgreSQL engine
engine = create_engine(
    DATABASE_URL
)



# Create database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)