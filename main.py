import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


SPOTIFY_USER_ID = 'to_replace'

class Billboard:

    def __init__(self, year):
        self.url = f'https://www.billboard.com/charts/hot-100/{year}'

    def fetch_tracks_title(self):
        tracks_title = []
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table_rows = soup.find_all(class_='chart-element__information__song')  
        for track in table_rows:
            track_title = track.get_text()
            tracks_title.append(track_title)
        return tracks_title

class Anghami:

    def __init__(self, url, cookies):
        self.url = url
        self.cookies = cookies
    
    def fetch_tracks_title(self):
        tracks_title = []
        response = requests.get(self.url, cookies=self.cookies)
        soup = BeautifulSoup(response.text, 'html.parser')
        table_rows = soup.find_all(class_='table-row')  
        for row in table_rows:
            track_title = row.select('.cell-title')[0].get_text()
            # artist_name = row.select('.cell-artist')[0].get_text()
            tracks_title.append(f'{track_title}')
        return tracks_title


class Spotify:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope = "playlist-modify-private",redirect_uri = "http://example.com",
                                    client_id = client_id, client_secret = client_secret, show_dialog = True, cache_path='token.txt') 
                                )
    def create_playlist(self, user_id, playlist_name):
        playlist = self.sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
        print(f'Playlist created.\n')
        return playlist
        
    def fetch_track_uris(self, tracks_title):
        track_uris = []
        for track_name in tracks_title:
            response = self.sp.search(q=f"track:{track_name}", type="track")
            try:
                uri = response["tracks"]["items"][0]["uri"]
                track_uris.append(uri)
            except IndexError:
                print(f"{track_name} doesn't exist in Spotify. Skipped.")
        return track_uris

    def add_tracks_to_playlist(self, playlist_id, tracks_uris, user_id):
        self.sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=tracks_uris)

if __name__ == "__main__":

    anghami_cookies = 'to_replace'

    # billboard = Billboard(year='2004-12-12')
    # billboard_tracks_title = billboard.fetch_tracks_title()
    # billboard_track_uris = spo.fetch_track_uris(billboard_tracks_title)
    anghami = Anghami('playlist_url', cookies=anghami_cookies)
    anghami_tracks_title = anghami.fetch_tracks_title()
    spo = Spotify(client_id='to_replace', client_secret='to_replace')
    playlist = spo.create_playlist(user_id=SPOTIFY_USER_ID, playlist_name='Anghami')
    anghami_track_uris = spo.fetch_track_uris(anghami_tracks_title)
    spo.add_tracks_to_playlist(playlist_id=playlist['id'], tracks_uris=anghami_track_uris, user_id=SPOTIFY_USER_ID)
