from . import get_db

def check_character_owner(user_id, character_id):
    db = get_db()
    character = get_character(character_id)


    if character is None or character.get('user_id') != user_id:
        return False
    
    return True

def add_new_character(character):
    db = get_db()
    keys = list(map(str, character.keys()))
    keys = ", ".join(keys)
    vals = list(character.values())
    question_marks = ", ".join(['?'] * len(vals))

    insert_statement = "INSERT INTO player_characters ({}) VALUES ({})".format(keys, question_marks)
    id = db.execute(insert_statement, vals).lastrowid
    db.commit()

    return id


def save_existing_character(character):
    db = get_db()
    id = character.pop('id')

    items = character.items()
    items = ["=".join(item) for item in items]
    items = ", ".join(items)

    update_statement = "UPDATE player_characters SET ({}) WHERE id = ?".format(items)

    db.execute(update_statement, id)

def get_character(character_id):
    db = get_db()
    character = db.execute("""
        SELECT * FROM player_characters WHERE id = ?
    """, character_id)

    return character

def get_all_characters(user_id):
    return []

def get_room_characters(room_id):
    return []
    

"""
        INSERT INTO player_characters VALUES (
                user_id, name, xp,

                background, race, alignment, ac, initiative, speed,

                hp_current, hp_maximum, hp_temporary, 
                hit_dice_current, hit_dice_total,
                death_save_succeses, death_save_failures,

                strength, dexterity, constitution, intelligence, wisdom, charisma,

                acrobatics, animal_handling, arcana, athletics, deception,
                history, insight, intimidation, investigation, medicine,
                nature, perception, performance, persuasion, religion,
                sleight_of_hand, stealth, survival,

                personality_traits, ideals, bonds, flaws)
    """