from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import words, search, stats

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.include_router(words.router)
app.include_router(search.router)
app.include_router(stats.router)
