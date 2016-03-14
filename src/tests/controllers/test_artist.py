from anillo.http.request import Request

from controllers.artist import Get, List, Create, Update, Delete, Like
from repositories.artist import create_artist, get_artist_by_id
from repositories.user import create_user
from errors.errors import get_response_error


def test_integration_get_artist_ok():
    request = Request()
    input_data = {
        'name': 'Duke Ellington',
        'biography': 'American composer, pianist and bandleader of a jazz orchestra.',
    }
    artist = create_artist(**input_data)
    # execute
    controller = Get()
    result = controller.get(request, artist.id)
    
    assert result['status'] == 200
    assert "artist" in result['body']
    assert result['body']['artist']['name'] == input_data['name']
    assert result['body']['artist']['biography'] == input_data['biography']


def test_integration_get_artist_fail():
    request = Request()
    # execute
    controller = Get()
    result = controller.get(request, 1)
    
    assert result['status'] == 400
    assert "id" in result['body']
    assert result['body']['id']['code'] == "ARTIST_ID_NOT_FOUND"


def test_integration_list_artist_ok():
    request = Request()
    input_data = {
        'name': 'Duke Ellington',
        'biography': 'American composer, pianist and bandleader of a jazz orchestra.',
    }
    artist = create_artist(**input_data)
    # execute
    controller = List()
    result = controller.get(request)
    
    assert result['status'] == 200
    assert "artists" in result['body']
    assert len(result['body']['artists']) == 1
    assert result['body']['artists'][0]['name'] == input_data['name']
    assert result['body']['artists'][0]['biography'] == input_data['biography']



def test_integration_create_artist_ok():
    request = Request()

    input_data = {
        'name': 'Duke Ellington',
        'biography': 'American composer, pianist and bandleader of a jazz orchestra.',
    }
    request['body'] = input_data

    # execute
    controller = Create()
    result = controller.post(request)
    
    assert result['status'] == 200
    assert "artist" in result['body']
    assert result['body']['artist']['name'] == input_data['name']
    assert result['body']['artist']['biography'] == input_data['biography']

    artist = get_artist_by_id(result['body']['artist']['id'])
    assert artist != None
    assert artist.name == input_data['name']
    assert artist.biography == input_data['biography']


def test_integration_create_artist_fail():
    request = Request()
    input_data = {
        'name': '',
        'biography': 'American composer, pianist and bandleader of a jazz orchestra.',
    }
    
    request['body'] = input_data

    # create artist
    artist = create_artist(**input_data)

    # execute
    controller = Create()
    result = controller.post(request)

    assert result['status'] == 400
    assert result['body']['name'] == get_response_error("CANT_BE_EMPTY")


def test_integration_update_artist_ok():
    request = Request()
    artist_data = {
        'name': 'Duke Ellington',
        'biography': 'American composer, pianist and bandleader of a jazz orchestra.',
    }
    # create artist
    artist = create_artist(**artist_data)

    update_data = {
        'name': 'Django Reinhardt',
        'biography': 'Belgian-born French guitarist and composer of Romani ethnicity.',
    }
    request['body'] = update_data

    # execute
    controller = Update()
    result = controller.put(request, id=artist.id)

    assert result['status'] == 200
    assert "artist" in result['body']
    assert result['body']['artist']['name'] == update_data['name']
    assert result['body']['artist']['biography'] == update_data['biography']

    artist = get_artist_by_id(result['body']['artist']['id'])
    assert artist != None
    assert artist.name == update_data['name']
    assert artist.biography == update_data['biography']


def test_integration_update_artist_fail():
    request = Request()
    update_data = {
        'name': 'Django Reinhardt',
        'biography': 'Belgian-born French guitarist and composer of Romani ethnicity.',
    }
    request['body'] = update_data

    # execute
    controller = Update()
    result = controller.put(request, id=1)

    assert result['status'] == 400
    assert "id" in result['body']
    assert result['body']['id']['code'] == "ARTIST_ID_NOT_FOUND"


def test_integration_delete_artist_ok():
    request = Request()
    artist_data = {
        'name': 'Duke Ellington',
        'biography': 'American composer, pianist and bandleader of a jazz orchestra.',
    }
    # create artist
    artist = create_artist(**artist_data)

    # execute
    controller = Delete()
    result = controller.delete(request, id=artist.id)

    assert result['status'] == 200
    assert 'deleted' in result['body']
    assert result['body']['deleted'] == True

    artist = get_artist_by_id(artist.id)
    assert artist == None


def test_integration_delete_artist_fail():
    request = Request()

    # execute
    controller = Delete()
    result = controller.delete(request, 1)
    assert result['status'] == 400
    assert "id" in result['body']
    assert result['body']['id']['code'] == "ARTIST_ID_NOT_FOUND"


def test_integration_like_artist_ok():
    request = Request()

    # create user
    user = create_user('test@test.com', '1234', '8c99f50fcb424c66b6e489d15461b781')
    like_data = {
        'user_id': user.id
    }
    request['body'] = like_data

    # create artist  
    artist_data = {
        'name': 'Duke Ellington',
        'biography': 'American composer, pianist and bandleader of a jazz orchestra.',
    }
    artist = create_artist(**artist_data)

    # execute
    controller = Like()
    result = controller.post(request, id=artist.id)

    assert result['status'] == 200
    assert "like" in result['body']
    assert result['body']['like'] == True


def test_integration_like_artist_fail():
    request = Request()

    # create user
    user = create_user('test@test.com', '1234', '8c99f50fcb424c66b6e489d15461b781')
    like_data = {
        'user_id': user.id
    }
    request['body'] = like_data

    # execute
    controller = Like()
    result = controller.post(request, id=1)

    assert result['status'] == 400
    assert "id" in result['body']
    assert result['body']['id']['code'] == "ARTIST_ID_NOT_FOUND"
