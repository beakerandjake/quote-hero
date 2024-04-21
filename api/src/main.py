from fastapi import FastAPI
from .routes import words, search, stats

app = FastAPI()
app.include_router(words.router)
app.include_router(search.router)
app.include_router(stats.router)
