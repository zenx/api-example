from entities.artist import Artist


def test_tojson_artist_ok():
    artist_data = {
        'name': 'Duke Ellington',
        'biography': 'American composer, pianist and bandleader of a jazz orchestra.',
    }
    artist = Artist(**artist_data)

    # execute
    json_artist = artist.toJSONDict()

    # assert
    assert len(json_artist) == 2
    assert 'name' in json_artist
    assert 'biography' in json_artist
    assert json_artist['name'] == artist_data['name']
    assert json_artist['biography'] == artist_data['biography']
