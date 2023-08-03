from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from main import app, get_db
import models
import schemas
import crud

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ensure the test database reflects the tables in the models
models.Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_database():
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)

def test_create_player():
    response = client.post(
        "/players/",
        json={
            "username": "player1", 
            "first_name": "Player", 
            "last_name": "One", 
            "middle_name": "Test", 
            "state": "active",
            "birthday": "1990-01-01",  
            "gender": "male", 
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "player1"
    assert data["first_name"] == "Player"
    assert data["last_name"] == "One"
    assert data["middle_name"] == "Test"
    assert data["state"] == "active"
    assert data["birthday"] == "1990-01-01"
    assert data["gender"] == "male"

def test_get_all_players():
    # Create players
    response = client.post(
        "/players/",
        json={
            "username": "player10", 
            "first_name": "Player", 
            "last_name": "Ten", 
            "middle_name": "Test", 
            "state": "active",
            "birthday": "1990-01-01",
            "gender": "male",
        },
    )
    assert response.status_code == 200

    response = client.post(
        "/players/",
        json={
            "username": "player11", 
            "first_name": "Player", 
            "last_name": "Eleven", 
            "middle_name": "Test", 
            "state": "active",
            "birthday": "1991-01-01",
            "gender": "male",
        },
    )
    assert response.status_code == 200

    # Get all players
    response = client.get("/players/")
    assert response.status_code == 200
    data = response.json()

    # Check the result
    assert any(player["username"] == "player10" for player in data)
    assert any(player["username"] == "player11" for player in data)


def test_get_player_by_username():
    # create a player
    response = client.post(
        "/players/",
        json={
            "username": "player1", 
            "first_name": "Player", 
            "last_name": "One", 
            "middle_name": "Test", 
            "state": "active",
            "birthday": "1990-01-01",
            "gender": "male",
        },
    )
    assert response.status_code == 200

    # retrieve the player by username
    response = client.get("/players/player1")
    assert response.status_code == 200
    assert response.json() == {
        "username": "player1", 
        "first_name": "Player", 
        "last_name": "One", 
        "middle_name": "Test", 
        "state": "active",
        "birthday": "1990-01-01",
        "gender": "male",
        "risk_scores": [],
    }