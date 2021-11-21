from yousician.extensions import mongo


class Rate(mongo.Document):
    song_id = mongo.StringField()
    rate = mongo.IntField()

    meta = {
        'indexes': [
            'song_id',
        ],
    }


class Song(mongo.Document):
    artist = mongo.StringField()
    title = mongo.StringField()
    difficulty = mongo.IntField()
    level = mongo.IntField()
    released = mongo.DateTimeField()

    meta = {
        'indexes': [
            'level',
            'title',
            'artist',
        ],
    }
