from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy import func
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from config import DATABASE_URL
from models import Repository

app = FastAPI()

# Database setup
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3466"],  # Adjust based on frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class RepositoryBase(BaseModel):
    name: str
    description: str
    url: str

class RepositoryResponse(RepositoryBase):
    id: int

    class Config:
        orm_mode = True

@app.get("/repositories/", response_model=dict)
async def get_repositories(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    query: str = Query(default=None, max_length=100),  # Allow None for query
    db: AsyncSession = Depends(get_db),
):
    # Build base query
    base_query = select(Repository)

    # If a search query is provided, filter by name or description
    if query:
        base_query = base_query.where(
            (Repository.name.ilike(f"%{query}%")) |
            (Repository.description.ilike(f"%{query}%"))
        )

    # Add pagination to the query
    paginated_query = base_query.offset(skip).limit(limit)

    # Execute the query
    result = await db.execute(paginated_query)
    repositories = result.scalars().all()

    # Fetch total count (with search filter if applicable)
    total_query = select(func.count(Repository.id)).select_from(base_query.subquery())
    total_count = await db.execute(total_query)
    total = total_count.scalar()

    # Return the response
    return {
        "repositories": [
            {
                "id": repo.id,
                "name": repo.name,
                "description": repo.description,
                "url": repo.url,
            }
            for repo in repositories
        ],
        "total": total,
    }


@app.post("/repositories/", response_model=RepositoryResponse)
async def create_repository(repo: RepositoryBase, db: AsyncSession = Depends(get_db)):
    # Validate uniqueness of repository by name
    existing_repo = await db.execute(select(Repository).where(Repository.name == repo.name))
    if existing_repo.scalars().first():
        raise HTTPException(status_code=400, detail="Repository already exists")

    new_repo = Repository(name=repo.name, description=repo.description, url=repo.url)
    db.add(new_repo)
    await db.commit()
    await db.refresh(new_repo)
    return new_repo

@app.delete("/repositories/{repository_id}/", response_model=dict)
async def delete_repository(repository_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Repository).where(Repository.id == repository_id))
    repo_to_delete = result.scalars().first()
    if not repo_to_delete:
        raise HTTPException(status_code=404, detail="Repository not found")

    await db.delete(repo_to_delete)
    await db.commit()
    return {"message": "Repository deleted successfully"}
