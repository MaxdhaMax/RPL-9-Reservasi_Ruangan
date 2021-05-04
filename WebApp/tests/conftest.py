import os
import tempfile

import pytest

from WebApp import create_app, db, bcrypt
from WebApp.config import TestConfig
from WebApp.model import User


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()  # looks like db.session.close() would work as well
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture(scope='module')
def new_user():
    username = "locationtest"
    password = "locationtest123"
    email = "locationtest@locat.com"
    hashedPassword = bcrypt.generate_password_hash(
        password).decode('utf-8')
    user = User(username=username, email=email, password=hashedPassword)
    return user
