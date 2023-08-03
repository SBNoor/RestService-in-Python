from fastapi import Depends, FastAPI, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas
from database import SessionLocal, engine
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

## Task 3: Add a new player to the database
@app.post("/players/",response_model=schemas.PlayerOut,summary='Creating a new player',description='Adding a new player to the database')
def add_player(player: schemas.PlayerBase,db: Session = Depends(get_db)):
    db_player = crud.get_player_by_username(db, player_username=player.username)
    if db_player:
        raise HTTPException(status_code=400, detail="Player already exists")
    return crud.add_player(db,player)

## Task 4: Add a risk score to a given player given a username
@app.post("/players/{player_username}/scores/",response_model=schemas.RiskScoreOut,summary='Adding a new risk score to a player',description='Adding a new risk score to a given player in the database')
def add_riskScore_to_player(player_username: str, risk_score: schemas.RiskScoreBase, db: Session = Depends(get_db)):
    db_player = crud.get_player_by_username(db,player_username=player_username)
    if db_player is None: 
        raise HTTPException(status_code=404, detail="Player does not exist")

    return crud.add_riskScore_to_player(db,player_username,risk_score)

## Task 5: Get risk scores for a given player
@app.get("/players/{player_username}/scores/",response_model=List[schemas.RiskScoreOut],summary='Getting list of scores',description='Retrieving a list of scores for a given player in the database')
def get_riskScores_for_a_player(player_username: str,db: Session = Depends(get_db)):
    db_player = crud.get_player_by_username(db,player_username=player_username)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player does not exist")

    return crud.get_riskScores_for_a_player(db,player_username, skip = 0,limit = 10)

## Task 6: Get all risk scores for all the players
@app.get("/players/scores/",response_model=List[schemas.AllPlayerScoreOut],summary='Retrieving scores of all the players',description='Retrieving scores of all the players from the database')
def get_scores_of_players(db: Session = Depends(get_db)):
    return crud.get_scores_of_players(db)

## Task 7: Get the state of a given player
@app.get("/players/{player_username}/state/",response_model=schemas.PlayerStateOut,summary='Retrive a given player states',description='retrieve a given player state from the database')
def get_player_state(player_username: str, db: Session = Depends(get_db)):    
    state = crud.get_player_state(db,player_username)
    if state is None:
        raise HTTPException(status_code=404, detail="Player does not exist")
    return state

## Task 8: Get the state of all the players
@app.get("/players/state/",response_model=List[schemas.AllPlayerStateOut],summary='Retrieving state of all the players',description='Retrieving state of all the players from the database')
def get_state_of_players(db: Session = Depends(get_db)):
    return crud.get_state_of_players(db)
    
## Task 9: Change the state of a given player
@app.patch("/players/{player_username}/state/",response_model=schemas.PlayerStateOut,summary='Change the state of the player', description='Change the state of the player in the database')
def change_player_state(player_username: str, db: Session = Depends(get_db)):
    state = crud.change_player_state(db,player_username)
    if state is None:
        raise HTTPException(status_code=404, detail='Player does not exist')
    return state

## Task 10: Delete a given player from the database
@app.delete("/players/{player_username}",response_model=schemas.PlayerOut,summary='Deleting a player',description='Removing a player from the database')
def delete_player(player_username: str, db: Session = Depends(get_db)):
    db_player = crud.get_player_by_username(db,player_username)
    if db_player is None:
        return HTTPException(status_code=404,detail='Player does not exist')
    return crud.delete_player(db, player_username)




