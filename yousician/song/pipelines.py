from typing import Dict, Union, Any, List


def max_min_average_rate_pipline(song_id: str) -> List[Union[
    Dict[str, Dict[str, Any]], Dict[str, Dict[str, Union[Dict[str, str], Dict[str, str], dict, Dict[str, str]]]]]]:
    pipline = [
        {"$match": {"song_id": song_id}},
        {
            "$group": {
                "_id": {},
                "min_rate": {"$min": "$rate"},
                "max_rate": {"$max": "$rate"},
                "average_rate": {"$avg": "$rate"},
            }
        },
    ]

    return pipline
