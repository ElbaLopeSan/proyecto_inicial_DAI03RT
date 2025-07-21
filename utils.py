import os
import base64
import json
from requests import post, get
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener las credenciales del archivo .env
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

# Verificar que las variables se cargaron correctamente
if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("CLIENT_ID y CLIENT_SECRET deben estar configurados en el archivo .env")

def get_token():
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result
    return token["access_token"]

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_playlist(token, playlist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={playlist_name}&type=playlist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_playlist(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_features(token, songs_id):
    url = f"https://api.spotify.com/v1/audio-features?ids={songs_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result