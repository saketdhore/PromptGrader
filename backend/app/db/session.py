from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the DATABASE_URL from your .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to Render PostgreSQL
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for your models
Base = declarative_base()
