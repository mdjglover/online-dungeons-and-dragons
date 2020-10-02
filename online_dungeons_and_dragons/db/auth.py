from . import get_db

def add_user(username, password, email):
    db = get_db()

    db.execute(
        'INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
        (username, password, email)
    )
    db.commit()

def get_user(identifier, identifier_type):
    """ 
    identifier is an id, username, email address.
    identifier_type must be in ['id', 'username', 'email'], otherwise returns None.
    """
    db = get_db()
    user = None

    if identifier_type == 'id':
        user = db.execute(
                'SELECT * FROM users WHERE id = ?', (identifier,)
            ).fetchone()
    elif identifier_type == 'username':
        user = db.execute(
                'SELECT * FROM users WHERE username = ?', (identifier,)
            ).fetchone()
    elif identifier_type == 'email':
        user = db.execute(
                'SELECT * FROM users WHERE email = ?', (identifier,)
            ).fetchone()
    
    return user

def get_user_id(identifier, identifier_type):
    """ 
    identifier is a username or email address.
    identifier_type must be in ['username', 'email'], otherwise returns None.
    """

    id = None
    user = get_user(identifier, identifier_type)
    
    if user is not None:
        id = user['id']
    
    return id