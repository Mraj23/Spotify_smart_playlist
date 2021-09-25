import requests 
from secret import *
import base64, json

 #curl -X "POST" -H "Authorization: Basic ZjM4ZjAw...WY0MzE=" -d grant_type=client_credentials https://accounts.spotify.com/api/token

authUrl = "https://accounts.spotify.com/api/token"

authHeader = {}
authData = {}

userID1 = input("Enter userID here :")
userID2 = input("Enter userID here :")


def getAccessToken(clientID, clientSecret):
    message = f"{clientID}:{clientSecret}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    print(base64_message)
    #Base64 Encode Client ID and Secret

    authHeader['Authorization'] = "Basic " + base64_message
    authData['grant_type'] = "client_credentials"
    res = requests.post(authUrl, headers = authHeader, data = authData)

    responseObject = res.json()
    
    accessToken = responseObject['access_token']

    return accessToken



def getPlaylistTracks(token, id):
    playlistEndPoint = "https://api.spotify.com/v1/playlists/"+id
    getHeader = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(playlistEndPoint, headers = getHeader)
    playlistObject = res.json()
    #print(json.dumps(playlistObject, indent = 2))

    return playlistObject


def getUserPlaylist(token, userID):
    playlistEndPoint =  f"https://api.spotify.com/v1/users/{userID}/playlists"
    getHeader = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(playlistEndPoint, headers = getHeader)
    playlistObject = res.json()
    return playlistObject


# API requests

#token = getAccessToken(clientID, clientSecret)
token = 'BQBJFXWIYykCNXbhhWVjOSr8OirPaZRmQL7ajkj25wXZN7nDG2CWfLrs2mqHCDJAEaC0R8qrka6Iaeue9Qqd1pVHs-h5T5jCqTqoZ00zrjN-kgVntzpFt_37zMmVhnR6s3xj7jkyn5vJH9RLNOR_LWSOZmyeQ9n_E7C5c3h70-l2Fn6Bsz2bbl2q0iOkGW2OfaG9bjg8WdVIY65ZjAJxvpxdNQTTCwnHB1JsoT5CMlq_RCnf7hp6dodjfM22DjygLw2N_y9LyJOsKHFjHF00'

#playlistID = "3jlQ8b1Jfzf5GfYZc32AUt?si=a02a758254974a87"

#userPlaylists = getUserPlaylist(token, userID)

#print(json.dumps(userPlaylists, indent = 2))


#tracklist = getPlaylistTracks(token, playlistID)

#print(json.dumps(tracklist, indent = 2))


def getPublicPlaylist(token, user):
    l = []
    tracklist = ""
    userPlaylists = getUserPlaylist(token, user)
    print(json.dumps(userPlaylists, indent = 2))

    for p in userPlaylists['items']:
        name = p['name']
        id2 = p['id']
        print(id2)
        print(name)
        print("***************")
        tt = getPlaylistTracks(token, id2)
        for t in tt['tracks']["items"]:
            print(t['track']['name'])
            tracklist += (t["track"]["uri"] + ",")
            #print(tracklist)
            l.append(t['track']['uri'])
        
    tracklist = tracklist[:-1]
    
    return l

def get_mutual(l1,l2):
    mutual_tracks = []
    for e in l1:
        if e in l2:
            mutual_tracks.append(e)
    return mutual_tracks

l1 = getPublicPlaylist(token, userID1)
l2 = getPublicPlaylist(token, userID2)

mutual = get_mutual(l1,l2)

def uri_string(l):
    uri_string = ""
    for e in l:
        uri_string += e + ','
    uri_string = uri_string[:-1]
    return uri_string

uris = uri_string(mutual)
print('hello this is mutual')
print(mutual)


            
endpoint_url = f"https://api.spotify.com/v1/users/{userID1}/playlists"
request_body = json.dumps({
          "name": "New playlist",
          "description": "My first programmatic playlist, yooo!",
          "public": True # let's keep it between us - for now
        })
response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json", 
                        "Authorization": f'Bearer {token}'})




playlist_id = response.json()['id']
playlist_id = '3jlQ8b1Jfzf5GfYZc32AUt'
uris = uri_string(mutual)
uris = 'spotify:track:2eMwDehkIC1j68U6FA3Eiq'

endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

request_body = json.dumps({
          "uris" : uris
        })

response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json", 
                        "Authorization":f'Bearer {token}'})


print(response.json)


'''def add_to_playlist(token, songID, playlistID):
    
    # add all songs to new playlist
    print("Adding songs...")
    
    query = f"https://api.spotify.com/v1/users/{playlistID}/tracks?uris={songID}"

    response = requests.post(query, headers={"Content-Type": "application/json",
                                                 "Authorization": "Bearer" + token})

    '''


#1116761818
#12150954305




#token = "BQCScnsEA68rGT143KmewICuz0mfKmwFMb7JhVjNVUo4QRNHbS"
#songID = 'spotify:track:1jJci4qxiYcOHhQR247rEU','spotify:track:6KuHjfXHkfnIjdmcIvt9r0'
#playlistID = "3jlQ8b1Jfzf5GfYZc32AUt"

#add_to_playlist(token, songID, playlistID)



