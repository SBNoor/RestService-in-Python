from sqlalchemy.orm import Session
import datetime
import models, schemas
from collections import defaultdict

def get_all_players(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Player).offset(skip).limit(limit).all()

def get_player_by_username(db: Session, player_username: str):
    return db.query(models.Player).filter(models.Player.username == player_username).first()

def add_player(db: Session, player: schemas.PlayerBase):
    db_player = models.Player(
        username = player.username,
        first_name = player.first_name,
        last_name = player.last_name,
        middle_name = player.middle_name,
        birthday = player.birthday,
        gender = player.gender,
        state = player.state,
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def add_riskScore_to_player(db: Session, player_username: str, risk_score: schemas.RiskScoreBase):
    db_risk_score = models.RiskScores(
        score=risk_score.score,
        player_username=player_username,
        created_at=datetime.datetime.now() 
    )
    db.add(db_risk_score)
    db.commit()
    db.refresh(db_risk_score)
    return db_risk_score

def get_riskScores_for_a_player(db: Session, player_username: str, skip: int = 0, limit: int = 10):
    return db.query(models.RiskScores).filter(models.RiskScores.player_username == player_username).offset(skip).limit(limit).all()

def get_player_state(db: Session, player_username: str):
    player = db.query(models.Player).filter(models.Player.username == player_username).first()
    if player is not None:
        return {
            "username": player.username,
            "first_name": player.first_name,
            "last_name": player.last_name,
            "middle_name": player.middle_name,
            "state": player.state
        }
    else:
        return None

def change_player_state(db: Session, player_username: str):
    player = db.query(models.Player).filter(models.Player.username == player_username).first()
    if player is None:
        return None
    if player.state == 'active':
        player.state = 'inactive'
        db.commit()
    elif player.state == 'inactive':
        player.state = 'active'
        db.commit()
    return {
        "username": player.username,
        "first_name": player.first_name,
        "last_name": player.last_name,
        "middle_name": player.middle_name,
        "state": player.state
    }

def delete_player(db: Session, player_username: str):
    player = db.query(models.Player).filter(models.Player.username == player_username).first()
    if player is None:
        return None
    db.delete(player)
    db.commit()
    return player

def get_state_of_players(db: Session):
    players = db.query(models.Player).all()
    return [
        {
            "username": player.username,
            "first_name": player.first_name,
            "last_name": player.last_name,
            "middle_name": player.middle_name,
            "state": player.state
        }
        for player in players
    ]

def get_scores_of_players(db: Session):
    players_scores = db.query(models.RiskScores).all()

    # Group scores by player_username
    grouped_scores = defaultdict(list)
    for score in players_scores:
        grouped_scores[score.player_username].append({"score": score.score, "created_at": score.created_at})

    return [{"username": username, "risk_scores": scores} for username, scores in grouped_scores.items()]
        

    


