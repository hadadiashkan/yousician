from application.extensions import mongo


class Rate(mongo.Document):
    song_id = mongo.StringField()
    rate = mongo.IntField()
