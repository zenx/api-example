from repositories.redis import r
from services.user import register
from services.artist import get, list, create, update, delete, like, unlike


artist_data = {
    'name': 'Duke Ellington',
    'biography': 'American composer, pianist and bandleader of a jazz orchestra.',
}


def test_create_artist_ok():
    created, data, errors = create(**artist_data)
    assert not errors
    assert created is True
    assert "artist" in data
    assert data['artist'].name == artist_data['name']
    assert data['artist'].biography == artist_data['biography']
    
    # check get artist
    ok, data, errors = get(data['artist'].id)
    assert ok is True


def test_create_artist_fail():
    created, data, errors = create(**artist_data)
    # try to create a second time
    created, data, errors = create(**artist_data)
    assert errors
    assert len(errors) == 1
    assert "name" in errors
    assert errors['name']['code'] == "ARTIST_NAME_ALREADY_EXISTS"


def test_update_artist_ok():
    # create artist first
    created, data, errors = create(**artist_data)

    new_artist_data = {
        'name': 'Django Reinhardt',
        'biography': 'Belgian-born French guitarist and composer of Romani ethnicity.',
    }

    # update artist
    updated, data, errors = update(data['artist'].id, **new_artist_data)

    assert not errors
    assert updated is True
    assert "artist" in data

    assert data['artist'].name != artist_data['name']
    assert data['artist'].biography != artist_data['biography']

    assert data['artist'].name == new_artist_data['name']
    assert data['artist'].biography == new_artist_data['biography']


def test_update_artist_fail():
    # create artist
    created, data, errors = create(**artist_data)

    new_artist_data = {
        'name': 'Django Reinhardt',
        'biography': 'Belgian-born French guitarist and composer of Romani ethnicity.',
    }

    # try to update artist with unexisting id
    unexisting_id = data['artist'].id + 1
    updated, data, errors = update(unexisting_id, **new_artist_data)

    assert errors
    assert len(errors) == 1
    assert "id" in errors
    assert errors['id']['code'] == "ARTIST_ID_NOT_FOUND"


def test_list_artist():
    artist_data_2 = {
        'name': 'Django Reinhardt',
        'biography': 'Belgian-born French guitarist and composer of Romani ethnicity.',
    }
    # create first artist
    created, data, errors = create(**artist_data)
    # create second artist
    created, data, errors = create(**artist_data_2)
    
    ok, data, errors = list()
    assert ok == True
    assert "artists" in data
    assert len(data['artists']) == 2

    assert data['artists'][0].name == artist_data['name']
    assert data['artists'][0].biography == artist_data['biography']

    assert data['artists'][1].name == artist_data_2['name']
    assert data['artists'][1].biography == artist_data_2['biography']


def test_delete_artist_ok():
    # create artist
    created, data, errors = create(**artist_data)

    # check artist was created
    assert created is True
    assert "artist" in data

    artist_id = data['artist'].id

    # check get artist
    ok, data, errors = get(artist_id)
    assert ok is True

    # delete artist
    deleted, data, errors = delete(artist_id)
    assert deleted == True
    assert not errors
    assert data == {}

    # try to get artist
    ok, data, errors = get(artist_id)
    assert ok is False
    assert errors
    assert len(errors) == 1
    assert "id" in errors
    assert errors['id']['code'] == "ARTIST_ID_NOT_FOUND"


def test_delete_artist_fail():
    # create artist
    created, data, errors = create(**artist_data)

    # check artist was created
    assert created is True
    assert "artist" in data
    
    # check get artist
    ok, data, errors = get(data['artist'].id)
    assert ok is True

    unexisting_id = data['artist'].id + 1

    # delete artist
    deleted, data, errors = delete(unexisting_id)
    assert deleted == False
    assert errors
    assert len(errors) == 1
    assert "id" in errors
    assert errors['id']['code'] == "ARTIST_ID_NOT_FOUND"


def test_like_unlike_artist_ok():
    # create artist
    created, data, errors = create(**artist_data)
    artist_id = data['artist'].id

    # create user
    created, data, errors = register('test@test.com', '1234')
    user_id = data['user'].id

    # like artist
    like(user_id, artist_id)

    # check user artist likes
    user_likes_key = 'user:{}:likes'.format(user_id)
    user_likes_artist_ids = r.smembers(user_likes_key)

    assert user_likes_artist_ids
    assert len(user_likes_artist_ids) == 1
    assert int(user_likes_artist_ids.pop()) == artist_id

    # unlike artist
    unlike(user_id, artist_id)

    # remove user artist like
    assert not user_likes_artist_ids
    assert len(user_likes_artist_ids) == 0
