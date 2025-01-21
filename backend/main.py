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
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API configuration from environment variables
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("AI_API_KEY")
DEEPSEEK_API_URL = os.getenv("AI_API_URL")

if not DEEPSEEK_API_KEY or not DEEPSEEK_API_URL:
    raise ValueError("DEEPSEEK_API_KEY and DEEPSEEK_API_URL must be set in the .env file")

# Initialize DeepSeek API client
deepseek_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_URL)

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
        from_attributes = True


@app.get("/repositories/", response_model=dict)
async def get_repositories(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    query: Optional[str] = Query(None, max_length=100),
    db: AsyncSession = Depends(get_db),
):
    base_query = select(Repository)

    if query:
        base_query = base_query.where(
            (Repository.name.ilike(f"%{query}%")) |
            (Repository.description.ilike(f"%{query}%"))
        )

    paginated_query = base_query.offset(skip).limit(limit)
    result = await db.execute(paginated_query)
    repositories = result.scalars().all()

    total_query = select(func.count(Repository.id)).select_from(base_query.subquery())
    total_count = await db.execute(total_query)
    total = total_count.scalar()

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
    existing_repo = await db.execute(select(Repository).where(Repository.name == repo.name))
    if existing_repo.scalars().first():
        raise HTTPException(status_code=400, detail="Repository already exists")

    new_repo = Repository(name=repo.name, description=repo.description, url=repo.url)
    db.add(new_repo)
    await db.commit()
    await db.refresh(new_repo)

    # Notify the AI system about the new repository
    try:
        messages = [
            {"role": "system", "content": "Notify AI about a new repository."},
            {"role": "user", "content": f"Repository created: {repo.name}. Description: {repo.description}. URL: {repo.url}"}
        ]
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        # Correctly access the AI response content
        ai_response = response.choices[0].message.content
        print(f"AI Response: {ai_response}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Notification Failed: {e}")

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
