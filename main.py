import os
import re
import json
import time
import base64
from requests import get, post

DATA_SOURCE_PATH = os.getenv('DATA_SOURCE_PATH')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def get_token():
    auth_string = CLIENT_ID + ':' + CLIENT_SECRET
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    result = post(
        url='https://accounts.spotify.com/api/token',
        headers={
            'Authorization': 'Basic ' + auth_base64,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data={
            'grant_type': 'client_credentials',
        },
    )

    return json.loads(result.content)['access_token']


def parse_tracks():
    with open('data', 'r') as file:
        token = get_token()
        tracks_list = []
        get_url = lambda track_id: 'https://api.spotify.com/v1/tracks/' + track_id
        headers = {
            'Authorization': 'Bearer ' + token,
        }
        tracks = file.readlines()

        seen_tracks = []
        size = len(tracks)

        for index, track_url in enumerate(tracks):
            print(f'Parsing track {index + 1} / {size}')
            track_id = re.split('/|\?', track_url)[-2]
            result = json.loads(get(url=get_url(track_id), headers=headers).content)
            track_name = result['name']

            if track_name in seen_tracks:
                print('Duplicate, skipping...')
                continue

            seen_tracks.append(track_name)
            track_artists = [artist['name'] for artist in result['artists']]
            tracks_list.append(
                {
                    'title': ', '.join(track_artists) + ' - ' + track_name,
                    'url': track_url.strip(),
                }
            )

            time.sleep(0.5)

    return list(sorted(tracks_list, key=lambda track: track['title'], reverse=False))


def format_tracks(tracks):
    markdown = ''

    for index, track in enumerate(tracks):
        markdown += f'{index + 1}. [{track["title"]}]({track["url"]})\n'

    return markdown


parsed_tracks = parse_tracks()
formatted_tracks = format_tracks(parsed_tracks)

with open('tracks.md', 'w') as file:
    file.write(formatted_tracks)
