class RatePipline:

    @staticmethod
    def max_min_average_rate_pipline(song_id):
        pipline = [
            {
                "$match": {
                    "song_id": song_id
                }
            },
            {
                "$group": {
                    "_id": {},
                    "min_rate": {
                        "$min": "$rate"
                    },
                    "max_rate": {
                        "$max": "$rate"
                    },
                    "average_rate": {
                        "$avg": "$rate"
                    }
                }
            }
        ]
        return pipline
