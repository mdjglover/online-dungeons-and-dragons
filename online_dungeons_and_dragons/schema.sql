DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS player_characters;
DROP TABLE IF EXISTS player_classes;
DROP TABLE IF EXISTS player_currency;
DROP TABLE IF EXISTS player_equipment;
DROP TABLE IF EXISTS player_features_and_traits;
DROP TABLE IF EXISTS player_proficiencies;
DROP TABLE IF EXISTS player_weapons;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS room_members;
DROP TABLE IF EXISTS room_dms;
DROP TABLE IF EXISTS room_characters;
DROP TABLE IF EXISTS messages;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE
);

CREATE TABLE rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_code TEXT NOT NULL UNIQUE,
    password TEXT,
    creator_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    room_name TEXT NOT NULL,
    FOREIGN KEY (creator_id) REFERENCES users (id)
);

CREATE TABLE player_characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    xp INTEGER NOT NULL DEFAULT 0,

    background TEXT NOT NULL DEFAULT '',
    race TEXT NOT NULL DEFAULT '',
    alignment TEXT NOT NULL DEFAULT '',
    armour_class INTEGER NOT NULL DEFAULT 10,
    initiative INTEGER NOT NULL DEFAULT 0,
    speed INTEGER NOT NULL DEFAULT 30,

    hp_current INTEGER NOT NULL DEFAULT 0,
    hp_maximum INTEGER NOT NULL DEFAULT 0,
    hp_temporary INTEGER NOT NULL DEFAULT 0,
    hit_dice_current TEXT NOT NULL DEFAULT "",
    hit_dice_total TEXT NOT NULL DEFAULT "",
    death_save_successes INTEGER NOT NULL DEFAULT 0,
    death_save_failures INTEGER NOT NULL DEFAULT 0,

    inspiration INTEGER NOT NULL DEFAULT 0,
    proficiency_bonus INTEGER NOT NULL DEFAULT 0,
    passive_perception INTEGER NOT NULL DEFAULT 0,

    strength INTEGER NOT NULL DEFAULT 10,
    dexterity INTEGER NOT NULL DEFAULT 10,
    constitution INTEGER NOT NULL DEFAULT 10,
    intelligence INTEGER NOT NULL DEFAULT 10,
    wisdom INTEGER NOT NULL DEFAULT 10,
    charisma INTEGER NOT NULL DEFAULT 10,

    saving_throw_strength BOOLEAN NOT NULL DEFAULT FALSE,
    saving_throw_dexterity BOOLEAN NOT NULL DEFAULT FALSE,
    saving_throw_constitution BOOLEAN NOT NULL DEFAULT FALSE,
    saving_throw_intelligence BOOLEAN NOT NULL DEFAULT FALSE,
    saving_throw_wisdom BOOLEAN NOT NULL DEFAULT FALSE,
    saving_throw_charisma BOOLEAN NOT NULL DEFAULT FALSE,

    acrobatics BOOLEAN NOT NULL DEFAULT FALSE,
    animal_handling BOOLEAN NOT NULL DEFAULT FALSE,
    arcana BOOLEAN NOT NULL DEFAULT FALSE,
    athletics BOOLEAN NOT NULL DEFAULT FALSE,
    deception BOOLEAN NOT NULL DEFAULT FALSE,
    history BOOLEAN NOT NULL DEFAULT FALSE,
    insight BOOLEAN NOT NULL DEFAULT FALSE,
    intimidation BOOLEAN NOT NULL DEFAULT FALSE,
    investigation BOOLEAN NOT NULL DEFAULT FALSE,
    medicine BOOLEAN NOT NULL DEFAULT FALSE,
    nature BOOLEAN NOT NULL DEFAULT FALSE,
    perception BOOLEAN NOT NULL DEFAULT FALSE,
    performance BOOLEAN NOT NULL DEFAULT FALSE,
    persuasion BOOLEAN NOT NULL DEFAULT FALSE,
    religion BOOLEAN NOT NULL DEFAULT FALSE,
    sleight_of_hand BOOLEAN NOT NULL DEFAULT FALSE,
    stealth BOOLEAN NOT NULL DEFAULT FALSE,
    survival BOOLEAN NOT NULL DEFAULT FALSE,

    personality_traits TEXT DEFAULT '',
    ideals TEXT DEFAULT '',
    bonds TEXT DEFAULT '',
    flaws TEXT DEFAULT '',

    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE player_classes (
    player_character_id INTEGER NOT NULL,
    class TEXT NOT NULL DEFAULT '',
    class_level INTEGER NOT NULL DEFAULT 1,

    FOREIGN KEY (player_character_id) REFERENCES player_characters (id)
);

CREATE TABLE player_proficiencies (
    player_character_id INTEGER NOT NULL,
    proficiency TEXT NOT NULL DEFAULT '',

    FOREIGN KEY (player_character_id) REFERENCES player_characters (id)
);

CREATE TABLE player_features_and_traits (
    player_character_id INTEGER NOT NULL,
    trait TEXT NOT NULL DEFAULT '',

    FOREIGN KEY (player_character_id) REFERENCES player_characters (id)
);

CREATE TABLE player_weapons (
    player_character_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,

    name TEXT NOT NULL,
    attack_bonus INTEGER NOT NULL DEFAULT 0,
    damage TEXT NOT NULL,

    PRIMARY KEY (player_character_id, room_id),
    FOREIGN KEY (player_character_id) REFERENCES player_characters (id),
    FOREIGN KEY (room_id) REFERENCES rooms (id)
);

CREATE TABLE player_equipment (
    player_character_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,

    name TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,

    PRIMARY KEY (player_character_id, room_id),
    FOREIGN KEY (player_character_id) REFERENCES player_characters (id),
    FOREIGN KEY (room_id) REFERENCES rooms (id)
);

CREATE TABLE player_currency (
    player_character_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,

    cp INTEGER NOT NULL DEFAULT 0,
    sp INTEGER NOT NULL DEFAULT 0,
    ep INTEGER NOT NULL DEFAULT 0,
    gp INTEGER NOT NULL DEFAULT 0,
    pp INTEGER NOT NULL DEFAULT 0,

    PRIMARY KEY (player_character_id, room_id),
    FOREIGN KEY (player_character_id) REFERENCES player_characters (id),
    FOREIGN KEY (room_id) REFERENCES rooms (id)
);


CREATE TABLE room_members (
    user_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,

    PRIMARY KEY (user_id, room_id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (room_id) REFERENCES rooms (id)
);

CREATE TABLE room_dms (
    room_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,

    FOREIGN KEY (room_id) REFERENCES rooms (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE room_characters (
    room_id INTEGER NOT NULL,
    player_character_id INTEGER NOT NULL,

    FOREIGN KEY (player_character_id) REFERENCES player_characters (id),
    FOREIGN KEY (room_id) REFERENCES rooms (id)
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    player_character_id INTEGER NOT NULL,

    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    message TEXT NOT NULL,

    FOREIGN KEY (room_id) REFERENCES rooms (id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (player_character_id) REFERENCES player_characters (id)
);