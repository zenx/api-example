from .session import session_manager as sm

from entities.album import Album
from repositories.persistence import AlbumTable


def create_album(title, artist):
    album_row = AlbumTable(
            title=title,
            artist=artist,
            likes=0)

    sm.session.add(album_row)
    sm.session.commit()
    return _album_row_to_album(album_row)


def update_album(id, title=None, artist=None, likes=None):
    album_row = _get_album_row_by_filter({'id': id})
    if album_row:
        if title:
            album_row.title = title
        if artist:
            album_row.artist = artist
        if likes:
            album_row.likes = likes

        sm.session.add(album_row)
        sm.session.commit()
        return True
    else:
        return False


def delete_album(id):
    album_row = _get_album_row_by_filter({'id': id})
    if album_row:
        sm.session.delete(album_row)
        sm.session.commit()
        return True
    else:
        return False


def get_album_by_id(id):
    album_row = sm.session.query(AlbumTable).get(id)
    return _album_row_to_album(album_row)


def get_album_by_artist_and_name(artist_id, name):
    album_row = _get_album_row_by_filter({"artist_id": artist_id, "name": name})
    return _album_row_to_album(album_row)


def get_albums():
    albums = sm.session.query(AlbumTable).all()
    return [_album_row_to_album(album_row) for album_row in albums]


def get_albums_by_artist(artist_id):
    albums = sm.session.query(AlbumTable).filter_by(artist_id=artist_id)
    return [_album_row_to_album(album_row) for album_row in albums]


def _get_album_row_by_filter(f):
    album_row = sm.session.query(AlbumTable).filter_by(**f).one_or_none()
    return album_row


def _album_row_to_album(album_row):
    if album_row:
        return Album(
                id=album_row.id,
                name=album_row.title,
                artist=album_row.artist,
                likes=album_row.likes)
    return None
