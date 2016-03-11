from .entity import Entity


class Album(Entity):
    def __init__(self, *args, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        self.title = kwargs['title']
        self.artist = kwargs['artist']
        self.likes = 0

    def __repr__(self):
        return "entities.Album: {}".format(self.title)

    def toJSONDict(self):
        return super(Album, self).toJSONDict(["title", "artist", "likes"])
