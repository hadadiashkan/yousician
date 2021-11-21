from flask import url_for

from yousician.song.models import Song, Rate

def test_get_songs(client):
    # test 404
    user_url = url_for('app_song.user_by_id')
    rep = client.get(user_url)
    assert rep.status_code == 404