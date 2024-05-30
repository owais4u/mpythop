from fastapi import FastAPI, HTTPException
from .db import get_user_by_id, create_user, Base, engine
from .models import User

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=User)
def add_user(user: User):
    return create_user(user)
