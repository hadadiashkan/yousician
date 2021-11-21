import json

from bson import json_util
from flask import Blueprint, request
from flask_restful import Api, Resource
from mongoengine import Q

from .models import Rate, Song
from .pipelines import RatePipline
from .schemas import SongSchema, RateValidator, RateSchema
from ..utils.pagination import paginate
from ..utils.response import custom_rest_response


class SongList(Resource):
    def get(self):
        message = request.args.get("message", "", type=str)

        songs_query = (
            Song.objects(
                Q(artist__icontains=message) | Q(title__icontains=message)
            )
            if message
            else Song.objects
        )
        paginated_data = {**paginate(songs_query, SongSchema(many=True))}
        return custom_rest_response(
            data=paginated_data,
            status_code=200 if paginated_data.get('total') else 404,
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

        # check song existence
        Song.objects.get_or_404(_id=song_id, message='Song Not Found!')

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
