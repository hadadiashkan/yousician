import json

from bson import json_util
from flask import Blueprint, request
from flask_restful import Api, Resource
from mongoengine import Q

from models.rate import Rate
from models.song import Song
from mongo_pipelines.rate import RatePipline
from schemas.rate import RateSchema, RateValidator
from schemas.song import SongSchema
from utils.response import custom_rest_response


class SongList(Resource):
    def get(self):
        limit = request.args.get("limit", 8, type=int)
        page = request.args.get("page", 1, type=int)

        message = request.args.get("message", "", type=str)

        songs = (
            Song.objects(
                Q(artist__icontains=message) | Q(title__icontains=message)
            ).paginate(page, limit)
            if message
            else Song.objects.paginate(page, limit)
        )
        return custom_rest_response(
            data={"songs": SongSchema(many=True).dump(songs.items), 'total': songs.total},
            status_code=200 if songs.items else 404,
        )


class SongListAnalytic(Resource):
    def get(self):
        level = request.args.get("level", 0, type=int)

        average_difficulty = (
            Song.objects(difficulty__gte=level).average("difficulty")
            if level
            else Song.objects.average("difficulty")
        )

        return custom_rest_response(data={"average_difficulty": average_difficulty}, status=200)


class RateSong(Resource):
    def get(self, song_id):
        rate_analytics = Rate.objects(song_id=song_id).aggregate(RatePipline.max_min_average_rate_pipline(song_id))

        return custom_rest_response(data=json.dumps(list(rate_analytics), default=json_util.default))

    def post(self, song_id):
        validated_data = RateValidator().load(request.get_json())
        rate = Rate(song_id=song_id, rate=validated_data.get('rating'))
        rate.save()

        return custom_rest_response(data={'rate': RateSchema().dump(rate)}, status_code=201)


def get_resources():
    """
    Returns app song resources.
    :param app: The Flask instance
    :return: App Song resources
    """
    blueprint = Blueprint("app_song", __name__, url_prefix="/api/v1")

    api = Api(blueprint)

    api.add_resource(SongList, "/songs")
    api.add_resource(SongListAnalytic, "/songs/average-difficulty")
    api.add_resource(RateSong, "/song/<string:song_id>/rate")

    return blueprint
