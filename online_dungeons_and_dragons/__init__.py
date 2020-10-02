import os

from flask import Flask, session
from flask_socketio import SocketIO, join_room, emit, send

socketio = SocketIO()

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'online_dungeons_and_dragons.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import user
    app.register_blueprint(user.bp)
    
    from . import rooms
    app.register_blueprint(rooms.bp)

    app.add_url_rule("/", endpoint="user.index")

    socketio.init_app(app)

    return app