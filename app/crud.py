from sqlalchemy.orm import Session
import datetime
import models, schemas ## my system
#from . import models, schemas ## for docker
from collections import defaultdict

def get_all_players(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Player).offset(skip).limit(limit).all()

def get_player_by_username(db: Session, player_username: str):
    return db.query(models.Player).filter(models.Player.username == player_username).first()

def create_player(db:Session, player: schemas.PlayerBase):
    db_player = models.Player(
        username = player.username,
        first_name =  player.first_name,
        last_name =  player.last_name,
        middle_name =  player.middle_name,
        birthday =  player.birthday,
        gender =  player.gender,
        state =  player.state,
    )

    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player
