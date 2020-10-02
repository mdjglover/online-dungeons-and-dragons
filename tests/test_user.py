import pytest
from flask import g, session, url_for
from online_dungeons_and_dragons.db import get_db
import json


def test_index(client, auth):
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/auth/login'
    auth.login()
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/user/home'

def test_home(client, auth):
    auth.login()
    response = client.get('/user/home')
    assert b'test1' in response.data

def test_create_character(client, auth):
    pass

def test_save_character(client, auth, default_character):
    auth.login()
    character = default_character
    character['name'] = 'Test'
    response = client.post('/user/save_character',
         data=json.dumps({'character': character, 'save_to_room': False, 'new_character': True}),
         content_type='application/json',
         )
    assert response.status_code == 200
    response_data = json.loads(response.get_data(as_text=True))
    assert 'id' in response_data



def test_get_characters(client, auth):
    pass

def test_get_room_characters(client, auth):
    pass
