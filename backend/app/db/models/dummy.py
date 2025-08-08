from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class DummyModel(Base):
    __tablename__ = "dummy_model"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
