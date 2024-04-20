from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return "Hello World"

while True:
    pass