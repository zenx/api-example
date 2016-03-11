from entities.artist import Artist
from entities.album import Album
from entities.song import Song


def test_tojson_song_ok():
    artist_data = {
        'name': 'Duke Ellington',
        'biography': 'American composer, pianist and bandleader of a jazz orchestra.',
    }
    artist_data_2 = {
        'name': 'Django Reinhardt',
        'biography': 'Belgian-born French guitarist and composer of Romani ethnicity.',
    }
    artist_1 = Artist(**artist_data)
    artist_2 = Artist(**artist_data_2)

    album_data = {
        'title': 'The Far East Suite',
        'artist': artist_1,
    }
    album = Album(**album_data)

    song_data = {
        'title': 'Mount Harissa',
        'album': album,
        'duration': 142,
        'featuring_artists': [artist_2]
    }
    song = Song(**song_data)
    
    # execute
    json_song = song.toJSONDict()

    # check song data
    assert len(json_song) == 4
    assert 'title' in json_song
    assert 'album' in json_song
    assert 'duration' in json_song
    assert 'featuring_artists' in json_song

    assert json_song['title'] == song_data['title']
    assert json_song['duration'] == song_data['duration']

    ## check song album data
    assert json_song['album']['title'] == album_data['title']
    
    # check artist data
    assert json_song['album']['artist']['name'] == artist_data['name']
    assert json_song['album']['artist']['biography'] == artist_data['biography']

    # check featuring artists data
    assert len(json_song['featuring_artists']) == 1
    assert json_song['featuring_artists'][0]['name'] == artist_data_2['name']
    assert json_song['featuring_artists'][0]['biography'] == artist_data_2['biography']
