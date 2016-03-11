from errors.errors import get_response_error
from repositories.user import get_user_by_uuid
from repositories.artist import create_artist, update_artist, delete_artist, \
                                get_artist_by_name, get_artist_by_id, get_artists, \
                                like_artist, unlike_artist, get_artist_likes_for_user, \
                                get_artists_by_similarity


def get(id):
    errors = {}
    artist = get_artist_by_id(id)
    if artist:
        return True, {"artist": artist}, None
    else:
        errors["id"] = get_response_error("ARTIST_ID_NOT_FOUND")

    if errors:
        return False, None, errors


def list():
    errors = {}
    artists = get_artists()
    return True, {'artists': artists}, None


def create(name, biography):
    errors = {}
    artist = get_artist_by_name(name)

    if artist:
        errors["name"] = get_response_error("ARTIST_NAME_ALREADY_EXISTS")
    else:
        artist = create_artist(name, biography)
        return True, {"artist": artist}, None

    if errors:
        return False, None, errors


def update(id, name, biography):
    errors = {}

    if update_artist(id, name, biography):
        # get updated artist
        artist = get_artist_by_id(id)
        return True, {"artist": artist}, None
    else:
        errors["id"] = get_response_error("ARTIST_ID_NOT_FOUND")

    if errors:
        return False, None, errors


def delete(id):
    errors = {}

    if delete_artist(id):
        return True, {}, None
    else:
        errors["id"] = get_response_error("ARTIST_ID_NOT_FOUND")

    if errors:
        return False, None, errors

    return create_artist(email, password)


def like(user_uuid, artist_id):
    errors = {}

    artist = get_artist_by_id(artist_id)
    if not artist:
        errors["id"] = get_response_error("ARTIST_ID_NOT_FOUND")
    else:
        if like_artist(user_uuid, artist_id):
            return True, {}, None
        else:
            return False, None, {}
    
    if errors:
        return False, None, errors


def unlike(user_uuid, artist_id):
    errors = {}

    artist = get_artist_by_id(artist_id)
    if not artist:
        errors["id"] = get_response_error("ARTIST_ID_NOT_FOUND")
    else:
        if unlike_artist(user_uuid, artist_id):
            return True, {}, None
        else:
            return False, None, {}


def get_user_artist_likes(user_uuid):
    artists = get_artist_likes_for_user(user_uuid)
    return True, {"artists": artists}, None


def get_similar_artists(id):
    artists = get_artists_by_similarity(id)
    return True, {"artists": artists}, None
