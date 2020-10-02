import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from online_dungeons_and_dragons.auth import login_required
from online_dungeons_and_dragons.db.rooms import (
    create_room as db_create_room, delete_room as db_delete_room, get_room, get_room_members, add_user_to_room, get_room_dms
)

from flask_socketio import emit, send, join_room as socketio_join_room, leave_room as socketio_leave_room
from . import socketio

from online_dungeons_and_dragons.util.dice_roll import generate_dice_roll_message, validate_dice_roll

bp = Blueprint('rooms', __name__, url_prefix='/rooms')

active_rooms = {}
connected_users = {}

@bp.route('/create_room', methods=('GET', 'POST'))
@login_required
def create_room():
    if request.method == 'POST':
        creator_id = session.get('user_id')
        room_name = request.form['room_name']
        password = request.form['password']
        
        error = None

        if not room_name:
            error = "Room name is required."
        
        if error is None:
            room_code = db_create_room(creator_id, room_name, generate_password_hash(password))
            return redirect(url_for('.room', room_code=room_code))
        
        flash(error)
    
    return render_template('rooms/create_room.html')


@bp.route('/<room_code>/delete_room', methods=('POST',))
@login_required
def delete_room(room_code):
    user_id = session.get('user_id')
    room = get_room(room_code)
    error = None

    if user_id != room['creator_id']:
        error = "You are not authorized to delete this room."
    
    if error is None:
        db_delete_room(room['id'])
        socketio.emit('kick_all', namespace='/room', room=room_code)
    else:
        flash(error)

    return redirect(url_for('user.home'))

@bp.route('/join_room', methods=('GET','POST'))
@login_required
def join_room():
    if request.method == 'POST':
        room_code = request.form['room_code']
        password = request.form['password']
        room = get_room(room_code)
        user_id = session.get('user_id')
        error = None

        if room_code is None:
            error = 'Room code is required.'
        elif password is None:
            error = 'Password is required.'
        elif room is None:
            error = 'Incorrect room code.'
        elif not check_password_hash(password, room['password']):
            error = 'Incorrect password.'
        
        if error is None:
            add_user_to_room(user_id, room['id'])
            return redirect(url_for('rooms.room', room_code=room_code))
        
        flash(error)

    return render_template('rooms/join_room.html')


@bp.route('/<room_code>/room', methods=('GET','POST'))
@login_required
def room(room_code):
    user_id = session.get('user_id')

    room = get_room(room_code)
    room_members = get_room_members(room['id'])
    room_dms = get_room_dms(room['id'])
    
    error = None

    if user_id not in room_members:
        error = "You are not a member of room {}.".format(room_code)

    if error is None:
        if room_code not in active_rooms:
            active_rooms[room_code] = room

        session['room_code'] = room_code
        session['room_id'] = room['id']
        
        return render_template('rooms/room.html', room=room)
     
    flash(error)
    return redirect(url_for('user.home'))

@socketio.on('connect')
def on_connect():
    #session['socketio_id'] = request.namespace.socket.sessid
    emit('status', {'msg':'User has connected.'})

@socketio.on('joined', namespace='/rooms')
def joined(message):
    room_code = session.get('room_code')
    socketio_join_room(room_code)
    emit('status', {'msg':'A party member has joined.'}, room=room_code)

@socketio.on('text', namespace='/rooms')
def on_text_received(message):
    room_code = session.get('room_code')

    error = None
    character = message.get('character_name')
    text = message.get('msg')

    if not character:
        error = 'Please enter a valid character name.'
    elif not text:
        error = 'Please enter a valid message.'

    if error is not None:
        print(error)
        return

    msg = '{}: {}'.format(character, text)
    emit('message', {'msg':msg}, room=room_code)

@socketio.on('dice_roll', namespace='/rooms')
def on_dice_roll(message):
    room_code = session.get('room_code')
    character = message.get('character_name')
    num_dice = message.get('num_dice')
    dice_type = message.get('dice_type')
    modifier = message.get('modifier')

    error = validate_dice_roll(character, num_dice, dice_type, modifier)
    
    if error is not None:
        print(error)
        return

    msg = generate_dice_roll_message(character, int(num_dice), int(dice_type), int(modifier))
    emit('message', {'msg':msg}, room=room_code)

