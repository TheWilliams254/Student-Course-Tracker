from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

from models import Base
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set. Check your .env file.")

engine = create_engine(DATABASE_URL)

# Create all tables
Base.metadata.create_all(engine)

print("✅ Tables created successfully.")
