import marshmallow as mar
import marshmallow_mongoengine as ma

from models.rate import Rate


class RateValidator(mar.Schema):
    rating = mar.fields.Integer(required=True)


class RateSchema(ma.ModelSchema):
    class Meta:
        model = Rate
