from anillo.handlers.routing import optionized_url as url, context


from controllers.index import Index
from controllers import user, artist

urls = [
    context("/api/v1", [
        url("/", Index(), methods=["get", "post"]),

        # user urls
        url("/login", user.Login(), methods=["post"]),
        url("/users", user.Register(), methods=["post"]),
        url("/users", user.List(), methods=["get"]),

        # artist urls
        url("/artists", artist.List(), methods=["get"]),
        url("/artists", artist.Create(), methods=["post"]),
        url("/artists/<int:id>", artist.Update(), methods=["put"]),
        url("/artists/<int:id>", artist.Delete(), methods=["delete"]),
        url("/artists/<int:id>", artist.Get(), methods=["get"]),
        url("/artists/<int:id>/like", artist.Like(), methods=["post"]),
        url("/artists/<int:id>/unlike", artist.Unlike(), methods=["post"]),
    ]),
]
