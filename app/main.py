from fastapi import FastAPI

from app.api import auth, post

app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(post.router, prefix="/post", tags=["post"])
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Auth Backend"}
