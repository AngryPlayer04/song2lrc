from musicxmatch_api import MusixMatchAPI
import json

api = MusixMatchAPI()

def fetcher(song):

    try:
        results = api.search_tracks(song, page = 1)


        if isinstance(results, str):
            results = json.loads(results)

        track_list = results["message"]["body"]["track_list"]

        songs = []
        for item in track_list:
            track = item["track"]
            songs.append({
                "id": track["track_id"],
                "titulo": track["track_name"],
                "artista": track["artist_name"],
            })

        return songs


    except Exception as e:
        
        return []


def search_lyrics(track_id):
    try:
        results = api.get_track_lyrics(track_id)
        

        if isinstance(results, str):
            results = json.loads(results)

        lyrics = (
            results.get("message", {})
            .get("body", {})
            .get("lyrics", {})
            .get("lyrics_body", "")
        )

        return lyrics or "Lyrics not found."

    except Exception as e:
        return "Error while searching"
