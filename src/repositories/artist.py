from .session import session_manager as sm

from entities.artist import Artist
from repositories.persistence import ArtistTable
from repositories.redis import r


def create_artist(name, biography=None):
    artist_row = ArtistTable(
            name=name,
            biography=biography)
    sm.session.add(artist_row)
    sm.session.commit()
    return _artist_row_to_artist(artist_row)


def update_artist(id, name=None, biography=None):
    artist_row = _get_artist_row_by_filter({'id': id})
    if artist_row:
        if name:
            artist_row.name = name
        if biography:
            artist_row.biography = biography

        sm.session.add(artist_row)
        sm.session.commit()
        return True
    else:
        return False


def delete_artist(id):
    artist_row = _get_artist_row_by_filter({'id': id})
    if artist_row:
        sm.session.delete(artist_row)
        sm.session.commit()
        return True
    else:
        return False


def get_artist_by_id(id):
    artist_row = sm.session.query(ArtistTable).get(id)
    return _artist_row_to_artist(artist_row)


def get_artist_by_name(name):
    artist_row = _get_artist_row_by_filter({"name": name})
    return _artist_row_to_artist(artist_row)


def get_artists():
    artists = sm.session.query(ArtistTable).all()
    return [_artist_row_to_artist(artist_row) for artist_row in artists]


def get_artists_by_similarity(artist_id, max_results=10):
    artist_likes_key = 'artist:{}:similar_artists'.format(artist_id)
    similar_artists_ids = r.zrange(artist_likes_key, 0, -1, desc=True)[:max_results]
    artists = sm.session.query(ArtistTable).filter(ArtistTable.id.in_(similar_artists_ids)).all()
    return [_artist_row_to_artist(artist_row) for artist_row in artists]


def get_artist_likes_for_user(user_uuid):
    artist_ids = r.smembers('user:{}:likes'.format(user_uuid))
    artists = sm.session.query(ArtistTable).filter(ArtistTable.id.in_(artist_ids)).all()
    return [_artist_row_to_artist(artist_row) for artist_row in artists]


def like_artist(user_uuid, artist_id):
    user_likes_key = 'user:{}:likes'.format(user_uuid)
    if not r.sismember(user_likes_key, artist_id):
        # artist not in user likes: add it
        r.sadd(user_likes_key, artist_id)
        # udpate artist likes
        user_artist_likes = [id for id in r.smembers(user_likes_key) if id != artist_id]
        _update_artist_likes(artist_id, user_artist_likes, 'like')
        return True
    return False


def unlike_artist(user_uuid, artist_id):
    user_likes_key = 'user:{}:likes'.format(user_uuid)
    if not r.sismember(user_likes_key, artist_id):
        # artist is in user likes: remove it
        user_likes_key = 'user:{}:likes'.format(user_uuid)
        r.srem(user_likes_key, artist_id)

        # udpate artist likes
        user_artist_likes = [id for id in r.smembers(user_likes_key) if id != artist_id]
        _update_artist_likes(artist_id, user_artist_likes, 'unlike')
        
        return True
    return False


def _update_artist_likes(artist_id, artist_ids, action):
    if action == 'like':
        amount = 1
    elif action == 'unlike':
        amount = -1

    # increment/decrement score for other artists related to artist_id
    artist_likes_key = 'artist:{}:similar_artists'.format(artist_id)
    for id in artist_ids:
        r.zincrby(artist_likes_key,
                  id,
                  amount=amount)

    # increment/decrement score for artist_id related to other artists
    for id in artist_ids:
        r.zincrby('artist:{}:similar_artists'.format(id),
                  artist_id,
                  amount=amount)


def _get_artist_row_by_filter(f):
    artist_row = sm.session.query(ArtistTable).filter_by(**f).one_or_none()
    return artist_row


def _artist_row_to_artist(artist_row):
    if artist_row:
        return Artist(
                id=artist_row.id,
                name=artist_row.name,
                biography=artist_row.biography)
    return None
