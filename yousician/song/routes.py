import json
from typing import Tuple, Union, Dict

from bson import json_util
from flask import Blueprint, request
from flask_restful import Api, Resource
from mongoengine import Q

from .models import Rate, Song
from .pipelines import max_min_average_rate_pipline
from .schemas import RateSchema, RateValidator, SongSchema
from ..utils.pagination import paginate
from ..utils.response import custom_rest_response


class SongList(Resource):
    def get(self):
        message = request.args.get("message", "", type=str)

        songs_query = (
            Song.objects(Q(artist__icontains=message) | Q(title__icontains=message))
            if message
            else Song.objects
        )
        paginated_data = {**paginate(songs_query, SongSchema(many=True))}
        return custom_rest_response(
            data=paginated_data,
            status_code=200 if paginated_data.get("total") else 404,
        )


class SongListAnalytic(Resource):
    def get(self):
        level = request.args.get("level", 0, type=int)

        average_difficulty = (
            Song.objects(difficulty__gte=level).average("difficulty")
            if level
            else Song.objects.average("difficulty")
        )

        return custom_rest_response(
            data={"average_difficulty": average_difficulty}, status=200
        )


class RateSong(Resource):
    def get(self, song_id: str) -> Tuple[Union[Dict[str, bool], Dict[str, Union[bool, Dict[str, str]]]], int]:
        rate_analytics = Rate.objects(song_id=song_id).aggregate(
            max_min_average_rate_pipline(song_id)
        )

        return custom_rest_response(
            data=json.dumps(list(rate_analytics), default=json_util.default)
        )

    def post(self, song_id: str) -> Tuple[Union[Dict[str, bool], Dict[str, Union[bool, Dict[str, str]]]], int]:
        validated_data = RateValidator().load(request.get_json())

        # check song existence
        Song.objects.get_or_404(id=song_id)

        rate = Rate(song_id=song_id, rate=validated_data.get("rating"))
        rate.save()

        return custom_rest_response(
            data={"rate": RateSchema().dump(rate)}, status_code=201
        )


def get_resources():
    """
    Returns app song resources.
    :param app: The Flask instance
    :return: App Song resources
    """
    blueprint = Blueprint("app_song", __name__, url_prefix="/api/v1")

    api = Api(blueprint)

    api.add_resource(SongList, "/songs", endpoint="song_list")
    api.add_resource(SongListAnalytic, "/songs/average-difficulty", endpoint="songs_analytics")
    api.add_resource(RateSong, "/song/<string:song_id>/rate", endpoint="rate")

    return blueprint
