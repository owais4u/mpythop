import pytest
from fastapi.testclient import TestClient
from hellopp.main import app
from hellopp.db import Base, engine, SessionLocal, User

client = TestClient(app)

@pytest.fixture(scope='function')
def db():
    Base.metadata.create_all(bind=engine)  # Create tables
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)  # Drop tables after test

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_read_user(db):  # Inject the db fixture
    user = User(id=1, name="John Doe", email="johndoe@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe", "email": "johndoe@example.com"}

def test_add_user():
    response = client.post("/users/", json={"id": 1, "name": "John Doe", "email": "johndoe@example.com"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe", "email": "johndoe@example.com"}
