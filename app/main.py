"""
Main app
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, leaderboard, masks, pharmacies, purchase_histories, users
from app.utils.database import Base, engine

# to get a string like this run:

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(pharmacies.router, prefix="/pharmacies", tags=["pharmacies"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
app.include_router(
    purchase_histories.router, prefix="/purchase_histories", tags=["purchase_histories"]
)
app.include_router(masks.router, prefix="/masks", tags=["masks"])
