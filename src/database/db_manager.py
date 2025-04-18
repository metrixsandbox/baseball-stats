from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .models import Base

DATABASE_URL = "sqlite:///baseball_stats.db"  # Change this to your database URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def init_db():
    """Initialize the database by dropping all tables and recreating them."""
    Base.metadata.drop_all(engine)  # Drop all existing tables
    Base.metadata.create_all(engine)  # Create all tables with new schema

def get_session():
    """Get a new database session."""
    return Session()

def add_record(session, record):
    """Add a new record to the database."""
    try:
        session.add(record)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error adding record: {e}")

def get_all_records(session, model):
    """Retrieve all records of a given model."""
    return session.query(model).all()

def update_record(session, record):
    """Update an existing record in the database."""
    try:
        session.merge(record)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating record: {e}")