import datetime
from bs4 import BeautifulSoup
import requests
import os
import dotenv


# import pprint


def get_users_date():
    date = input("Which date do you want to travel back to? Type in YYYY-MM-DD format:\n")
    return date


def get_billboard_100(this_date):
    print(f"Date being searched: {this_date}")
    billboard_100_response = requests.get(f"https://www.billboard.com/charts/hot-100/{this_date}/")
    billboard_100_response.raise_for_status()
    billboard_100_page = BeautifulSoup(billboard_100_response.text, "html.parser")
    song_classes = [("c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet "
                     "lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis "
                     "u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet"),
                    ("c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet "
                     "lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis "
                     "u-max-width-330 u-max-width-230@tablet-only")]
    song_element_list = billboard_100_page.find_all(name="h3", class_=song_classes)
    song_list = [song_el.text.replace('\n', '').replace('\t', '') for song_el in song_element_list]
    print(f"Number of songs: {len(song_list)}")
    return song_list


def add_songs_to_playlist(song_title_list):
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth

    dotenv.load_dotenv()
    spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_secret = os.getenv("SPOTIFY_SECRET")
    spotify_redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

    scope = "playlist-modify-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                                   client_secret=spotify_secret,
                                                   scope=scope,
                                                   redirect_uri=spotify_redirect_uri))
    current_user = sp.current_user()
    # print(current_user)

    song_uris = []
    for song in song_title_list:
        query_string = f"track: {song}"
        song_response = sp.search(q=query_string, type="track", limit=1)
        # pprint.pprint(song_response, indent=4)
        # print(song_response['tracks']['items'][0]['id'])
        try:
            song_to_add = song_response['tracks']['items'][0]['id']
            song_uris.append(song_to_add)
        except IndexError:
            pass

    # print(song_uris)

    created_playlist = sp.user_playlist_create(user=current_user['id'], name=f'{chosen_date} Billboard 100',
                                               public=False,
                                               description=f'All the Billboard 100 hits from {chosen_date}')

    print(created_playlist)
    # sp.user_playlist_add_tracks(user=current_user['id'], playlist_id, tracks, position=None)


chosen_date = input("Which date do you want to travel back to? Type in YYYY-MM-DD format:\n")

while True:
    try:
        datetime.datetime.strptime(chosen_date, '%Y-%m-%d')
    except ValueError:
        chosen_date = input("Wrong date format. Type in YYYY-MM-DD format:\n")
    else:
        break

billboard_100_song_list = get_billboard_100(this_date=chosen_date)
add_songs_to_playlist(song_title_list=billboard_100_song_list)
