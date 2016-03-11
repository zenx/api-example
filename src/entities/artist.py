from .entity import Entity


class Artist(Entity):
    def __init__(self, *args, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        self.name = kwargs['name']
        self.biography = kwargs['biography']

    def __repr__(self):
        return "entities.Artist: {}".format(self.name)

    def toJSONDict(self):
        return super(Artist, self).toJSONDict(["id", "name", "biography"])
