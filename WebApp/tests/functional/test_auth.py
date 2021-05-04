import pytest
from flask_login import current_user

from WebApp import db


def test_register(client, app):
    # test that viewing the page renders without template errors
    assert client.get("/register").status_code == 200

    # test that successful registration redirects to the login page
    response = client.post(
        "/register",
        data={"username": "tstngserver", "email": "tstngserver@gmail.com",
              "password": "tstngserver", "passwordConfirmation": "tstngserver"},
        follow_redirects=True)
    assert b"login" in response.data


def test_login(client):
    # test that viewing the page renders without template errors
    assert client.get("/login").status_code == 200

    # test that successful login redirects to the index page
    response = client.post(
        '/login',
        data={"username": "tstngserver", "password": "tstngserver"},
        follow_redirects=True)
    assert response.status_code == 200

    # login request set the user_id in the session
    # check that the user is loaded from the session
    assert b'login' not in response.data


def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 200
    assert current_user == None
