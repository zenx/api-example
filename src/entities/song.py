from .entity import Entity


class Song(Entity):
    def __init__(self, *args, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        self.title = kwargs['title']
        self.duration = kwargs['duration']
        self.album = kwargs['album']
        self.featuring_artists = kwargs['featuring_artists']

    def __repr__(self):
        return "entities.Song: {}".format(self.title)

    def toJSONDict(self):
        return super(Song, self).toJSONDict(["title", "duration", "album", "featuring_artists"])
