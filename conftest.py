import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from permissions import PermissionManager
from Views import Views
from Controllers import Controller, Menu
from Models import Base, Group


@pytest.fixture(scope='session')
def test_engine():
    """Create a separate database engine for testing."""
    test_engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(test_engine)
    return test_engine


@pytest.fixture(scope='function')
def session(test_engine):
    """Create a new database session for each test."""
    connection = test_engine.connect()
    transaction = connection.begin()

    TestSessionLocal = sessionmaker(bind=connection)
    session = TestSessionLocal()

    # create default groups
    Management = Group(group_name="Management")
    Commercial = Group(group_name="Commercial")
    Support = Group(group_name="Support")

    session.add(Management)
    session.add(Commercial)
    session.add(Support)

    session.commit()

    with patch('Models.model_base.SessionLocal', return_value=session):
        yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope='function', autouse=True)
def setup_environment(monkeypatch):
    """Fixture to set up environment variables for the test environment."""
    monkeypatch.setenv('DB_USER', 'test_user')
    monkeypatch.setenv('DB_PWD', 'test_password')
    monkeypatch.setenv('DB_HOST', 'localhost')
    monkeypatch.setenv('DB_PORT', '3306')
    monkeypatch.setenv('DB_NAME', 'test_database')


@pytest.fixture
def app(session):
    """Provide the app instance with a mock session."""
    view = Views()
    permissions = PermissionManager()
    menu = Menu(view, permissions, session=session)
    app = Controller(view, menu)
    return app
