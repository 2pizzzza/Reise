from fastapi import FastAPI
from app.api import auth, users

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Auth Backend"}
