from . import get_db
from random import randint


def get_room(room_code):
    db = get_db()

    room = db.execute(
        "SELECT * FROM rooms WHERE room_code = ?", (room_code,)
        ).fetchone()
    
    return room

def create_room(creator_id, room_name, password):
    db = get_db()

    room_code = get_new_room_code()

    db.execute(
        "INSERT INTO rooms (creator_id, room_code, room_name, password) VALUES (?, ?, ?, ?)", (creator_id, room_code, room_name, password)
    )
    db.commit()

    room = db.execute(
        "SELECT * FROM rooms WHERE room_code = ?", (room_code,)
    ).fetchone()

    room_id = room['id']
    db.execute(
        "INSERT INTO room_members (user_id, room_id) VALUES (?, ?)", (creator_id, room_id) 
    )
    db.commit()

    db.execute(
        "INSERT INTO room_dms (user_id, room_id) VALUES (?, ?)", (creator_id, room_id)
    )
    db.commit()

    return room_code

def delete_room(room_id):
    db = get_db()

    db.execute(
        'DELETE FROM room_dms WHERE room_id = ?', (room_id,)
    )
    db.execute(
        'DELETE FROM room_members WHERE room_id = ?', (room_id,)
    )
    db.execute(
        'DELETE FROM rooms WHERE id = ?', (room_id,)
    )
    db.commit()

def add_user_to_room(user_id, room_id):
    db = get_db()
    
    db.execute(
        "INSERT INTO room_members (user_id, room_id) VALUES (?, ?)", (user_id, room_id)
    )
    db.commit()

def add_dm_to_room(user_id, room_id):
    db = get_db()
    
    db.execute(
        "INSERT INTO room_dms (user_id, room_id) VALUES (?, ?)", (user_id, room_id)
    )
    db.commit()

def get_room_members(room_id):
    db = get_db()

    room_members_rows = db.execute(
        "SELECT * FROM room_members WHERE room_id = ?", (room_id,)
    ).fetchall()

    room_members = []
    for row in room_members_rows:
        room_members.append(row['user_id'])

    return room_members

def get_room_dms(room_id):
    db = get_db()

    room_members = db.execute(
        "SELECT * FROM room_dms WHERE room_id = ?", (room_id,)
    ).fetchall()

    return room_members
    

def get_new_room_code():
    db = get_db()

    room_code = ""
    while True:
        room_code = generate_room_code()
        if get_room(room_code) is None:
            break
    
    return room_code

def generate_room_code():
    CODE_ELEMENTS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    CODE_LENGTH = 6

    room_code = ""

    for _ in range(CODE_LENGTH):
        room_code += CODE_ELEMENTS[randint(0, len(CODE_ELEMENTS)-1)]
    
    return room_code

def get_joined_rooms(user_id):
    db = get_db()

    joined_rooms = db.execute(
        'SELECT * FROM rooms WHERE id IN (SELECT room_id FROM room_members WHERE user_id = ?)', (user_id,)
    )

    return joined_rooms