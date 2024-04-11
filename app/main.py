from fastapi import FastAPI

from . import models
from .database import engine
from .routers import user, post, login, vote
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# models.Base.metadata.create_all(bind=engine)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(post.router)
app.include_router(login.router)
app.include_router(vote.router)

