# models.py

#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///student-tracker.db')

Base = declarative_base()