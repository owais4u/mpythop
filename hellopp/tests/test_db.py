import pytest
from hellopp.db import create_user, get_user_by_id, User, Base, engine, SessionLocal
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope='function')
def db():
    Base.metadata.create_all(bind=engine)  # Create tables
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)  # Drop tables after test

def test_create_user(db):  # Inject the db fixture
    user = User(id=1, name="John Doe", email="johndoe@example.com")
    db_user = create_user(user)
    assert db_user.id == user.id
    assert db_user.name == user.name
    assert db_user.email == user.email

def test_get_user_by_id(db):  # Inject the db fixture
    user = User(id=1, name="John Doe", email="johndoe@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    fetched_user = get_user_by_id(1)
    assert fetched_user.id == user.id
    assert fetched_user.name == user.name
    assert fetched_user.email == user.email
