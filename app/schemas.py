from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional, List
from enum import Enum as pyEnum

class Gender(str, pyEnum):
    male = 'male'
    female = 'female'
    others = 'others'

class State(str, pyEnum):
    active = 'active'
    inactive = 'inactive'

class PlayerCommon(BaseModel):
    username: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None

    @validator('username', 'first_name', 'last_name', 'middle_name', pre=True, always=True)
    def ensure_string(cls, value, field):
        if not isinstance(value, str):
            raise ValueError(f"{field.alias} must be a string, not {type(value).__name__}")
        return value

class PlayerBase(PlayerCommon):
    birthday: date
    gender: Gender
    state: State

    class Config:
        orm_mode = True
        extra = "forbid" 

class RiskScoreBase(BaseModel):
    score: float = Field(..., ge=0, le=100)

    class Config:
        orm_mode = True
        extra = "forbid" 

class RiskScoreOut(RiskScoreBase):
    created_at: datetime

class PlayerOut(PlayerBase):
    risk_scores: List[RiskScoreOut] = []

class PlayerStateOut(PlayerCommon):
    state: State

class AllPlayerStateOut(PlayerCommon):
    state: State

class AllPlayerScoreOut(BaseModel):
    username: str
    risk_scores: List[RiskScoreOut] = []
