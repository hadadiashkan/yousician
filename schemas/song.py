import marshmallow_mongoengine as ma

from models.song import Song


class SongSchema(ma.ModelSchema):
    class Meta:
        model = Song
