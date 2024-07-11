from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "sqlite:///./database.db"

engine = create_engine(db_url)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

