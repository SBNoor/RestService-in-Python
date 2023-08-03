from pydantic import BaseModel, Field
from datetime import date,datetime
from typing import Optional, List
from enum import Enum as pyEnum


class Gender(str,pyEnum):
    male = 'male'
    female = 'female'
    others = 'others'

class State(str,pyEnum):
    active = 'active'
    inactive = 'inactive'

class PlayerBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    birthday: date
    gender: Gender
    state: State

    class Config:
        orm_mode = True

class RiskScoreBase(BaseModel):
    score: float = Field(...,ge=0,le=100)

    class Config:
        orm_mode = True

class RiskScoreOut(RiskScoreBase):
    created_at: datetime

class PlayerOut(PlayerBase):
    risk_scores: List[RiskScoreOut] = []
    
class PlayerStateOut(BaseModel):
    username: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    state: State

class AllPlayerStateOut(BaseModel):
    username: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    state: State

class AllPlayerScoreOut(BaseModel):
    username: str
    risk_scores: List[RiskScoreOut] = []