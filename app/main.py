from fastapi import Depends, FastAPI, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas ## laptop
#from . import crud, models, schemas ## docker
from database import SessionLocal, engine
#from app.database import SessionLocal, engine ## docker
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

"""
/Users/noor/opt/anaconda3/bin/python
"""

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get('/')
def root():
    return {'Mindway AI Software Task'}

## Task 1: Getting all players
@app.get("/players/",response_model=List[schemas.PlayerOut],summary='Retrieve all players',description='Get all players from the database')
def get_all_players(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return crud.get_all_players(db,skip,limit)

## Task 2: Get a specific player given a username
@app.get("/players/{player_username}",response_model=schemas.PlayerOut,summary='Retrieve a specific player',description='Get a speific player given a usernamr from the database')
def get_player_by_username(player_username: str, db: Session = Depends(get_db)):
    db_player = crud.get_player_by_username(db, player_username=player_username)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player does not exist")
    return db_player

# Task 3: Add a new player
@app.post("/players/",response_model=schemas.PlayerOut,summary='Creating a new player',description='Adding a new player to the database')
def create_player(player: schemas.PlayerBase,db: Session = Depends(get_db)):
    db_player = crud.get_player_by_username(db, player_username=player.username)
    if db_player:
        raise HTTPException(status_code=404, detail="Player exists")

    return crud.create_player(db,player)