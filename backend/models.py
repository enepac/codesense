from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    url = Column(String)

# Pydantic models for request/response
class RepositoryCreate(BaseModel):
    name: str
    description: str
    url: str

class RepositoryResponse(BaseModel):
    id: int
    name: str
    description: str
    url: str

    class Config:
        orm_mode = True
