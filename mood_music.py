import pylast
import spotipy
from recommender.api import Recommender
from spotipy.oauth2 import SpotifyClientCredentials
import os, sys


class mood_search_by_api:

    # 極性値を入力
    def __init__(self, value):
        self.sentiment_value = value

    def search_by_lastfm(self):

        AK = os.environ["API_KEY"]
        AS = os.environ["API_SECRET"]

        username = os.environ["user"]
        password_hash = os.environ["password"]

        network = pylast.LastFMNetwork(api_key=AK, api_secret=AS, username=username, password_hash=password_hash)

        arrays = network.get_tag(name="sad")
        print(arrays)

        """
        for f in range(len(arrays)):
        print(arrays)

        """


    def search_by_spotify(self):
        # クライアントキー
        client_id = os.environ["spotify_ci"]
        client_secret = os.environ["spotify_cs"]

        # これはspotipyでうまくいかなかったバージョン
        # client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
        # spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        # results = spotify.recommendations(seed_genres="j-pop",country="JP",limit=1,target_valence=valence)
        # print(results)

        # spotifyへのリクエスト，キーをセット
        recommender = Recommender(client_id=client_id,
                                  client_secret=client_secret)

        # とりあえず日本の曲だけで
        recommender.market = "JP"
        recommender.genres = ["j-pop", "j-rock", "j-idol"]

        # センチメント値を入力
        recommender.track_attributes = {
            'target_valence': self.sentiment_value
        }
        # 結果を返すのは1曲でいい
        recommender.limit = 1
        # リクエスト
        recommendations = recommender.find_recommendations()
        # print(recommendations)

        # 曲，アーティスト，視聴urlをセット
        artist = recommendations["tracks"][0]['artists'][0]['name']
        song = recommendations["tracks"][0]['name']
        url = recommendations["tracks"][0]['preview_url']

        # 視聴リクエストがないならSpotifyのページ
        if url == "None ":
            url =recommendations["tracks"][0]["artists"][0]["external_urls"]["spotify"]
        print("{} - {} - {}".format(song, artist, url))


        # 返り値はリストで
        return [song, artist, url]
