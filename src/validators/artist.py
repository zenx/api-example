from skame.schemas import strings as s, base as b

from errors.errors import get_response_error
from .validator import Validator


class ArtistValidator(Validator):
    key_name = 'artist_data'
    __schema__ = b.schema({
        'name': s.NotEmpty(get_response_error("CANT_BE_EMPTY")),
        'biography': s.NotEmpty(get_response_error("CANT_BE_EMPTY")),
    })

    def __init__(self, data: dict):
        super().__init__(data)
        if self.cleaned_data:
            self.name = self.cleaned_data['name']
            self.biography = self.cleaned_data['biography']

