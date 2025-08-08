from sqlalchemy import Column, Integer, String, Text, UniqueConstraint
from app.db.base_class import Base

class SystemInstructions(Base):
    __tablename__ = "system_instructions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role = Column(String, nullable=False) #grader, refiner, engineer, consultant,
    type = Column(String, nullable=False) #master, clarity, specificity, etc.
    instructions = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("role", "type", name="uq_role_type"),
        {"sqlite_autoincrement": True},
    )
