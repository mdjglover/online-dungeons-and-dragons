import pytest
from flask import session

from online_dungeons_and_dragons.db import get_db
from tests.conftest import AuthActions

@pytest.mark.parametrize("path", ("/rooms/create_room", "/rooms/AAAAAA/delete_room", "/rooms/join_room", "/rooms/AAAAAA/room"))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "http://localhost/auth/login"

def test_room(client, auth):
    response = auth.login()

    with client:
        assert client.get('/rooms/AAAAAA/room').status_code == 200
        assert 'room_code' in session
        assert session['room_code'] == 'AAAAAA'

    assert client.get('/rooms/BBBBBB/room').status_code == 302

def test_join_room(client, auth, app):
    response = auth.login()
    assert client.get('/rooms/join_room').status_code == 200
    response2 = client.post(
        '/rooms/join_room',
        data={'room_code': 'BBBBBB', 'password':''}
    )
    with app.app_context():
        assert get_db().execute(
            'SELECT * FROM room_members WHERE room_id = 2 AND user_id = 1'
        ).fetchone() is not None
    
    assert client.get('rooms/BBBBBB/room').status_code == 200


def test_create_room(client, auth, app):
    response = auth.login()
    assert client.get('/rooms/create_room').status_code == 200
    response2 = client.post('/rooms/create_room', data={
        'room_name':'room', 'password':'password'
    })
    with app.app_context():
        db = get_db()
        room = db.execute(
            'SELECT * FROM rooms WHERE room_name = "room"'
        ).fetchone()
        assert room is not None

        assert db.execute(
            'SELECT * FROM room_members WHERE room_id = {}'.format(room['id'])
        ).fetchone() is not None

        assert db.execute(
            'SELECT * FROM room_dms WHERE room_id = {}'.format(room['id'])
        ).fetchone() is not None

def test_delete_room(client, auth, app):
    auth.login()
    response = client.post('/rooms/AAAAAA/delete_room')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/user/home'

    with app.app_context():
        db = get_db()
        assert db.execute(
            'SELECT * FROM rooms WHERE id = 1'
        ).fetchone() is None
        assert db.execute(
            'SELECT * FROM room_members WHERE room_id = 1'
        ).fetchone() is None
        assert db.execute(
            'SELECT * FROM room_dms WHERE room_id = 1'
        ).fetchone() is None

def test_connected_event(client, auth, app, socketio):
    io_client = socketio.test_client(app, namespace='/', flask_test_client=client)
    assert io_client.is_connected()
    response = io_client.get_received()
    assert len(response) == 1

def test_joined_room_event(client, auth, app, socketio):
    with client:
        auth.login()
        page = client.get('/rooms/AAAAAA/room')
        io_client = socketio.test_client(app, namespace='/rooms', flask_test_client=client)
        io_client2 = socketio.test_client(app, namespace='/rooms', flask_test_client=app.test_client())

        assert io_client.is_connected()
        response = io_client.get_received()
        assert len(response) == 1

        assert io_client2.is_connected()
        response = io_client2.get_received()
        assert len(response) == 1

        io_client.emit('joined', {}, namespace='/rooms')
        response = io_client.get_received('/rooms')
        assert len(response) == 1

        response = io_client2.get_received('/rooms')
        assert len(response) == 0

def test_send_message_event(client, auth, app, socketio):
    auth.login()
    page = client.get('/rooms/AAAAAA/room')
    io_client = socketio.test_client(app, namespace='/rooms', flask_test_client=client)

    io_client.emit('joined', {}, namespace='/rooms')
    io_client.get_received('/rooms')

    io_client.emit('text', {'character_name':'test_character', 'msg':'test'}, namespace='/rooms')
    reponse = io_client.get_received('/rooms')
    assert len(reponse) == 1

def test_dice_roll_event(client, auth, app, socketio):
    auth.login()
    page = client.get('/rooms/AAAAAA/room')
    io_client = socketio.test_client(app, namespace='/rooms', flask_test_client=client)

    io_client.emit('joined', {}, namespace='/rooms')
    io_client.get_received('/rooms')

    io_client.emit('dice_roll', {'character_name':'test_character', 'num_dice':'1', 'dice_type':'20', 'modifier':'0'}, namespace='/rooms')
    response = io_client.get_received('/rooms')
    assert len(response) == 1
    msg = response[0]['args']['msg']
    assert 'test_character' in msg
    assert '1d20' in msg
    assert '+0' in msg
    assert 'Rolls' in msg
    assert 'Total' in msg

