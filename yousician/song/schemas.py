import marshmallow as mar
import marshmallow_mongoengine as ma

from .models import Rate, Song


class SongSchema(ma.ModelSchema):
    class Meta:
        model = Song


class RateValidator(mar.Schema):
    rating = mar.fields.Integer(required=True)


class RateSchema(ma.ModelSchema):
    class Meta:
        model = Rate
