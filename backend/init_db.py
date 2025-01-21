import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from models import Base  # Ensure this matches the location of your models
from config import DATABASE_URL  # Ensure this matches your configuration file

async def init_db():
    # Create the database engine
    engine = create_async_engine(DATABASE_URL, echo=True)

    # Initialize database schema
    async with engine.begin() as conn:
        print("Initializing database...")
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())
