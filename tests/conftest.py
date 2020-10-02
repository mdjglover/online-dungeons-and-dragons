import os
import tempfile

import pytest
import flask_socketio
from online_dungeons_and_dragons import create_app, socketio as app_socketio
from online_dungeons_and_dragons.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def socketio(app):
    socketio = app_socketio
    return socketio

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client
    
    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )
    
    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)

@pytest.fixture
def default_character():
    character = {
        'name': "",
        'background': "",
        'race': "",
        'alignment': "",
        'xp': 0,
        'personality_traits': "",
        'ideals': "",
        'bonds': "",
        'flaws': "",

        'hp_current': 0,
        'hp_maximum': 0,
        'hp_temporary': 0,
        'armour_class': 0,
        'initiative': 0,
        'speed': 0,
        'hit_dice_current': "",
        'hit_dice_total': "",
        'death_save_successes': 0,
        'death_save_failures': 0,
        'saving_throw_strength': False,
        'saving_throw_dexterity': False,
        'saving_throw_constitution': False,
        'saving_throw_intelligence': False,
        'saving_throw_wisdom': False,
        'saving_throw_charisma': False,

        'inspiration': 0,
        'proficiency_bonus': 0,
        'passive_perception': 0,
        'strength': 10,
        'dexterity': 10,
        'constitution': 10,
        'intelligence': 10,
        'wisdom': 10,
        'charisma': 10,
        'acrobatics': False,
        'animal_handling': False,
        'arcana': False,
        'athletics': False,
        'deception': False,
        'history': False,
        'insight': False,
        'intimidation': False,
        'investigation': False,
        'medicine': False,
        'nature': False,
        'perception': False,
        'performance': False,
        'persuasion': False,
        'religion': False,
        'sleight_of_hand': False,
        'stealth': False,
        'survival': False
        }
    return character