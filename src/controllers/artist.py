from anillo.http import Ok, BadRequest

from controllers.controller import Controller
from utils.authorization import login_required
from validators.validator import with_validators

from validators.artist import ArtistValidator, ArtistLikeValidator
from services.artist import list, create, update, get, delete, like, unlike, \
                            get_user_artist_likes, get_similar_artists


class Get(Controller):
    def get(self, request, id):
        success, result, errors = get(id)

        if not success:
            return BadRequest(errors)

        return Ok({"artist": result["artist"].toJSONDict()})


class List(Controller):
    def get(self, request):
        success, result, errors = list()

        if not success:
            return BadRequest(errors)

        return Ok({'artists': [u.toJSONDict() for u in result['artists']]})


class Create(Controller):
    @with_validators([ArtistValidator])
    def post(self, request, data):
        success, result, errors = create(
                data["artist_data"].name,
                data["artist_data"].biography
        )
        if not success:
            return BadRequest(errors)

        return Ok({"artist": result["artist"].toJSONDict()})


class Update(Controller):
    @with_validators([ArtistValidator])
    def put(self, request, data, id):
        success, result, errors = update(
                id,
                data["artist_data"].name,
                data["artist_data"].biography
        )
        if not success:
            return BadRequest(errors)

        return Ok({"artist": result["artist"].toJSONDict()})


class Delete(Controller):
    def delete(self, request, id):
        success, result, errors = delete(id)

        if not success:
            return BadRequest(errors)

        return Ok({"deleted": True})


class Like(Controller):
    @with_validators([ArtistLikeValidator])
    def post(self, request, data, id):
        success, result, errors = like(data["like_data"].user_id, id)

        if not success:
            return BadRequest(errors)

        return Ok({"like": True})


class Unlike(Controller):
    @with_validators([ArtistLikeValidator])
    def post(self, request, data, id):
        success, result, errors = like(data["like_data"].user_id, id)

        if not success:
            return BadRequest(errors)

        return Ok({"unlike": True})
