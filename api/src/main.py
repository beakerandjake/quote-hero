from fastapi import FastAPI
from .routes import words, search

app = FastAPI()
app.include_router(words.router)
app.include_router(search.router)
