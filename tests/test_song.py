from flask import url_for


def test_get_songs(testapp):
    # test 404
    songs_url = url_for('app_song.song_list')
    rep = testapp.get(songs_url)
    assert rep.status_code == 200
