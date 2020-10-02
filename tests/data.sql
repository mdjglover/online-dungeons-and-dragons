INSERT INTO users (username, email, password)
  VALUES
  ('test', 'test@test.it', 'pbkdf2:sha256:150000$uYUvRAli$646f2b43894010811190a370befb37971bf7cefbf72faadf89ac2c17449c4213'),
  ('user', 'user@user.us', 'pbkdf2:sha256:150000$jni9LYty$f240b6f775dee4c97df67b0fc4de70f562a4177f4b462ade643fe064b7f2b703');

INSERT INTO rooms (room_code, password, creator_id, room_name)
  VALUES 
  ('AAAAAA', 'a', 1, 'test1'),
  ('BBBBBB', '', 2, 'test2');

INSERT INTO rooms (room_code, creator_id, room_name)
  VALUES 
  ('CCCCCC', 1, 'test3');

INSERT INTO room_members (user_id, room_id)
  VALUES 
  (1, 1),
  (2, 2);

INSERT INTO room_dms (user_id, room_id)
  VALUES
  (1, 1),
  (2, 2);