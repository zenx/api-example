from entities.artist import Artist
from entities.album import Album


def test_tojson_album_ok():
    artist_data = {
        'name': 'Duke Ellington',
        'biography': 'American composer, pianist and bandleader of a jazz orchestra.',
    }
    artist = Artist(**artist_data)

    album_data = {
        'title': 'The Far East Suite',
        'artist': artist
    }
    album = Album(**album_data)

    # execute
    json_album = album.toJSONDict()

    # check album data
    assert len(json_album) == 3
    assert 'title' in json_album
    assert 'artist' in json_album
    assert 'likes' in json_album
    assert json_album['title'] == album_data['title']
    assert json_album['likes'] == 0

    # check album artist data
    assert json_album['artist']['name'] == artist_data['name']
    assert json_album['artist']['biography'] == artist_data['biography']
