from anillo.http import Ok, BadRequest

from controllers.controller import Controller
from utils.authorization import login_required
from validators.validator import with_validators

from validators.artist import ArtistValidator
from services.artist import list, create, update, get, delete, like, unlike, \
                            get_user_artist_likes, get_similar_artists


class Get(Controller):
    #@login_required
    def get(self, request):
        success, result, errors = create()

        if errors:
            return BadRequest(errors)

        return Ok({'users': [u.toJSONDict() for u in result['users']]})


class List(Controller):
    #@login_required
    def get(self, request):
        success, result, errors = list()

        if errors:
            return BadRequest(errors)

        return Ok({'users': [u.toJSONDict() for u in result['users']]})


class Create(Controller):
    #@login_required
    @with_validators([ArtistValidator])
    def post(self, request, data):
        success, result, errors = create(
                data["artist_data"].name,
                data["artist_data"].biography
        )
        if errors:
            return BadRequest(errors)

        return Ok(result)


class Update(Controller):
    #@login_required
    @with_validators([ArtistValidator])
    def put(self, request, id, data):
        success, result, errors = update(
                data["artist"].id,
                data["artist"].name,
                data["artist"].biography
        )
        if errors:
            return BadRequest(errors)

        return Ok(result)


class Delete(Controller):
    #@login_required
    def delete(self, request, id):
        success, result, errors = delete(id)

        if errors:
            return BadRequest(errors)

        return Ok(result)


class Like(Controller):
    #@login_required
    def post(request, id):
        # get user
        user = request.get('identity')
        success, result, errors = like(user.uuuid, id)

        if errors:
            return BadRequest(errors)

        return Ok(result)


class Unlike(Controller):
    #@login_required
    def post(request, id):
        # get user
        user = request.get('identity')
        success, result, errors = unlike(user.uuuid, id)

        if errors:
            return BadRequest(errors)

        return Ok(result)
