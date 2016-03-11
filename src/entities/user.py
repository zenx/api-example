from .entity import Entity

class User(Entity):
    def __init__(self, *args, **kwargs):
        if 'id' in kwargs:
            self.id = ['id']
        self.email = kwargs['email']
        self.password = kwargs['password']
        self.uuid = kwargs['uuid']
        if 'enabled' in kwargs:
            self.enabled = kwargs['enabled']

    def __repr__(self):
        return "entities.User: {}".format(self.email)

    def toJSONDict(self):
        return super(User, self).toJSONDict(["id", "uuid", "email", "enabled"])
