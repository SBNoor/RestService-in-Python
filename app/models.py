from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Date, DateTime, Float,Index
from sqlalchemy.orm import relationship 
from database import Base
from enum import Enum as pyEnum
import datetime

class Player(Base):
    __tablename__ = 'players'

    username = Column(String,primary_key=True,index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String,nullable=False)
    middle_name = Column(String)
    birthday = Column(Date,nullable=False)
    gender = Column(Enum('male','female','others'),nullable=False)
    state = Column(Enum('active','inactive'),nullable=False)

    risk_scores = relationship('RiskScores',back_populates='player',cascade="all, delete-orphan")

class RiskScores(Base):
    __tablename__ = 'scores'

    id = Column(Integer,primary_key=True,index=True)
    player_username = Column(String,ForeignKey("players.username", ondelete="CASCADE"),index=True)
    score = Column(Float,nullable=False)
    created_at = Column(DateTime,default=datetime.datetime.utcnow,index=True)

    player = relationship('Player',back_populates='risk_scores')

# Create compound index on player_username and created_at
Index('idx_username_createdat', RiskScores.player_username, RiskScores.created_at)
