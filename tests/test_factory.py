from online_dungeons_and_dragons import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing