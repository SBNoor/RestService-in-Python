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

def test_add_riskScore_to_player():
    # create a player
    response = client.post(
        "/players/",
        json={
            "username": "player2", 
            "first_name": "Player", 
            "last_name": "Two", 
            "middle_name": "Test", 
            "state": "active",
            "birthday": "1990-01-01",
            "gender": "male",
        },
    )
    assert response.status_code == 200

    # add risk score to the player
    response = client.post(
        "/players/player2/scores/",
        json={"score": 80.5},
    )
    assert response.status_code == 200
    assert "created_at" in response.json()
    assert response.json()["score"] == 80.5


def test_get_riskScores_for_a_player():
    # create a player
    response = client.post(
        "/players/",
        json={
            "username": "player3", 
            "first_name": "Player", 
            "last_name": "Three", 
            "middle_name": "Test", 
            "state": "active",
            "birthday": "1990-01-01",
            "gender": "male",
        },
    )
    assert response.status_code == 200

    # add risk score to the player
    response = client.post(
        "/players/player3/scores/",
        json={"score": 90.5},
    )
    assert response.status_code == 200

    # get risk scores for the player
    response = client.get("/players/player3/scores/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert "created_at" in response.json()[0]
    assert response.json()[0]["score"] == 90.5

def test_get_scores_of_all_players():
    # Create player
    response = client.post(
        "/players/",
        json={
            "username": "player8", 
            "first_name": "Player", 
            "last_name": "Eight", 
            "middle_name": "Test", 
            "state": "active",
            "birthday": "1990-01-01",
            "gender": "male",
        },
    )
    assert response.status_code == 200

    # Add risk score
    response = client.post("/players/player8/scores/", json={"score": 90.0})
    assert response.status_code == 200

    # Get all players scores
    response = client.get("/players/scores/")
    assert response.status_code == 200
    data = response.json()

    # Check the result
    assert any(player["username"] == "player8" and player["risk_scores"][0]["score"] == 90.0 for player in data)

def test_get_player_state():
    # create a player
    response = client.post(
        "/players/",
        json={
            "username": "player4", 
            "first_name": "Player", 
            "last_name": "Four", 
            "middle_name": "Test", 
            "state": "active",
            "birthday": "1990-01-01",
            "gender": "male",
        },
    )
    assert response.status_code == 200

    # get state of the player
    response = client.get("/players/player4/state/")
    assert response.status_code == 200
    assert response.json()["state"] == "active"

def test_get_state_of_all_players():
    # create a player
    response = client.post(
        "/players/",
        json={
            "username": "player5", 
            "first_name": "Player", 
            "last_name": "Five", 
            "middle_name": "Test", 
            "state": "active",
            "birthday": "1990-01-01",
            "gender": "male",
        },
    )
    assert response.status_code == 200

    # get state of all players
    response = client.get("/players/state/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert any(player["username"] == "player5" and player["state"] == "active" for player in response.json())

def test_change_player_state():
    # create a player
    response = client.post(
        "/players/",
        json={
            "username": "player6", 
            "first_name": "Player", 
            "last_name": "Six", 
            "middle_name": "Test", 
            "state": "active",
            "birthday": "1990-01-01",
            "gender": "male",
        },
    )
    assert response.status_code == 200

    # change the state of the player
    response = client.patch("/players/player6/state/", json={"state": "inactive"})
    assert response.status_code == 200
    assert response.json()["state"] == "inactive"

def test_delete_player():
    # create a player
    response = client.post(
        "/players/",
        json={
            "username": "player7", 
            "first_name": "Player", 
            "last_name": "Seven", 
            "middle_name": "Test", 
            "state": "active",
            "birthday": "1990-01-01",
            "gender": "male",
        },
    )
    assert response.status_code == 200

    # delete the player
    response = client.delete("/players/player7")
    assert response.status_code == 200

    # check if the player was deleted
    response = client.get("/players/player7")
    assert response.status_code == 404