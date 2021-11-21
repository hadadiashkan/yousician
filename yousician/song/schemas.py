import marshmallow as mar
import marshmallow_mongoengine as ma

from .models import Rate, Song


class SongSchema(ma.ModelSchema):
    class Meta:
        model = Song


class RateValidator(mar.Schema):
    rating = mar.fields.Integer(required=True)

    @mar.validates_schema
    def validate_rating(self, data: dict, **kwargs: dict) -> dict:
        rating = data.get('rating')
        if rating and (rating < 1 or rating > 5):
            raise mar.ValidationError({'error': 'rating m be between 1 and 5.'})

        return data


class RateSchema(ma.ModelSchema):
    class Meta:
        model = Rate
