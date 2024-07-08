from sqlalchemy import Column, String, Float, Text, REAL
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Items(Base):
    __tablename__ = "itemdata"
    id = Column(Text, primary_key=True, index=True)
    lat = Column(REAL, index=True, nullable=True)
    long = Column(REAL, index=True, nullable=True)
    userId = Column(Text, nullable=True)
    description = Column(String, nullable=True)
    price = Column(Float, index=True)
    status = Column(String, nullable=True)