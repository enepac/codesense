from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for your frontend's origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3466"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to CodeSense Backend"}

@app.get("/api/test")
async def test_api():
    return {"status": "success", "data": "Connected to backend!"}

