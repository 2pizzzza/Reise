from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.api import auth, post, photo

app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(post.router, prefix="/post", tags=["post"])
app.include_router(photo.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Auth Backend"}
