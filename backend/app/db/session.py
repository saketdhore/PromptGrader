from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from app.db.base_class import Base
from app.db.models.user import User
from app.db.models.prompt import Prompt
load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

# 👇 This is the async engine for asyncpg
engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)

# 👇 Async session factory
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

