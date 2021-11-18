from application.extensions import mongo


class Song(mongo.Document):
    artist = mongo.StringField()
    title = mongo.StringField()
    difficulty = mongo.IntField()
    level = mongo.IntField()
    released = mongo.DateTimeField()
