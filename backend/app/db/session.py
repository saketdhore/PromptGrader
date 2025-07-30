from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# 👇 This is the async engine for asyncpg
engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)

# 👇 Async session factory
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# 👇 Base for models (same as before)
Base = declarative_base()
