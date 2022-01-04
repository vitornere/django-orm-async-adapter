import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope='function')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        from scripts import PopulateDB, CleanDB
        CleanDB()
        PopulateDB()


@pytest.fixture(scope='function')
def client(db):
    from app import app
    client = TestClient(app)
    return client
