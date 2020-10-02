from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for, jsonify
)

from json import loads

from online_dungeons_and_dragons.auth import login_required
from online_dungeons_and_dragons.db.rooms import get_joined_rooms
from online_dungeons_and_dragons.db.user import get_all_characters, get_room_characters, save_existing_character, add_new_character

bp = Blueprint('user', __name__, url_prefix='/user')

class PlayerCharacter():
    def __init__(self, name):
        self.name = name

@bp.route('/')
def index():
    if g.user is None:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('user.home'))

@bp.route('/home', methods=('GET',))
@login_required
def home():
    user_id = session.get('user_id')
    rooms = get_joined_rooms(user_id)
    characters = get_all_characters('user_id')
    return render_template('user/home.html', joined_rooms=rooms, characters=characters)

@bp.route('/create_character', methods=('GET','POST'))
@login_required
def create_character():
    if request.method == 'POST':
        pass

    return render_template('user/create_character.html')

@bp.route('/<int:id>/character', methods=('GET','POST'))
@login_required
def character():
    pass

@bp.route('/get_characters', methods=['GET'])
@login_required
def get_characters():
    pass

@bp.route('<room_code>/get_characters', methods=['GET'])
@login_required
def get_room_characters():
    pass

@bp.route('save_character', methods=['POST'])
@login_required
def save_character():
    #TODO: Make less fragile, scrub character of any keys not to go into db

    # data: {
    #       'new_character': bool,
    #       'add_to_room': bool,
    #       'character': character{},
    #       }

    user_id = session.get('user_id')

    data = request.get_json()

    new_character = data.get('new_character')
    add_to_room = data.get('add_to_room')
    character = data.get('character')

    if new_character:
        character['user_id'] = user_id
        character_id = add_new_character(character)
        return jsonify(id=character_id)
    else:
        save_existing_character(character)