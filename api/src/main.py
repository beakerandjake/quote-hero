from fastapi import FastAPI
from .routes import words

app = FastAPI()
app.include_router(words.router)
