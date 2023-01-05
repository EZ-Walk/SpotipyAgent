import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

# Globals
scopes = 'user-read-currently-playing user-library-read playlist-modify-public'

def select_songs(songInfo): # Takes in an artist URI and the nth top played song to return. returns the URI of the artist's nth most played song
    topTracks = sp.artist_top_tracks(songInfo['artistsURIs'][0])
    # print(topTracks['tracks'][0]['name'])
    
    cSong = songInfo['uri']
    songs = set()
    if cSong != topTracks['tracks'][0]['uri']: # if the artist's most played track is not the same as the target song:
        songs.add(topTracks['tracks'][0]['uri']) # we add the artist's top song to our list to be returned
        print('Added "{}" to [songs]'.format(topTracks['tracks'][0]['name']))
    else:
        topTracks['tracks'][1]['uri'] # otherwise we add the second most played song
        print('Added "{}" to [songs]'.format(topTracks['tracks'][1]['name']))

    # we want to go through the rest of the list and if we find a song on the same album, add it to songs
    for s in topTracks['tracks']:
        if s['album']['name'] == songInfo['albumName']: # We found a song in the artist's top10 that is in the same album
            if s['name'] == songInfo['name']:
                continue
            else:
                songs.add(s['uri'])
                print('Added "{}" to [songs]'.format(s['name']))
                break

    print('[songs] contains {} songs'.format(songs))
    return songs

def get_current_info(song): # takes the response from current_user_playing_track()
    relevant_info = {}
    
    name = song['item']['name']
    relevant_info['name'] = name
    uri = song['item']['uri']
    relevant_info['uri'] = uri
    # print('Song name:\t\t', name)
    # print('Song uri:\t\t', uri)
    # print()
    
    artists = []
    artistURIs = []
    # loop thru artists and get some info
    for a in song['item']['artists']:
        artists.append(a['name'])
        artistURIs.append(a['uri'])
    #
    # print('Artists:\t\t', ', '.join(artists))
    relevant_info['artists'] = artists
    # print('Artist URIs:\t\t', ', '.join(artistURIs))
    relevant_info['artistsURIs'] = artistURIs
    
    albumType = song['item']['album']['album_type']
    relevant_info['albumType'] = albumType
    albumName = song['item']['album']['name']
    relevant_info['albumName'] = albumName
    albumURI = song['item']['album']['uri']
    relevant_info['albumURI'] = albumURI
    
    return relevant_info

def delete_all_songs():
    return

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print('Missing Argument, "username"')
        sys.exit()

    token = util.prompt_for_user_token(username, scopes, client_id='411ed1fc291749ccaf9523138836a2dd',client_secret='d5597fa540c84aa9ade5859bba91b681',redirect_uri='http://trythis/callback')
    sp = spotipy.Spotify(auth=token)

    if token:
        # Check for playlist existance
        userPlaylists = sp.user_playlists(username)
        for pl in userPlaylists['items']:
            if pl['name'] == 'TRY~THIS':
                plExists = True
                plID = pl['id']
                break
        # plExists will now be True if the playlist exists in the user's library

        if not plExists:
            # The playlist does not exist, we should create it
            sp.user_playlist_create(username, 'TRY~THIS', description="Auto filled using dark magic.")
        
        # if sys.argv[2] == 'reset':
        #     print('Resetting the playlist')
        #     delete_all_songs()


        # Go into selection of process to execute based on argv[2]
        current_song = sp.current_user_playing_track()
        print('Song: ', current_song['item']['name'])
        songInfo = get_current_info(current_song)
        songsToAdd = select_songs(songInfo)
        sp.user_playlist_add_tracks(username, plID, songsToAdd)



    else:
        print('Couldn\'t retrieve token for user, "{}"'.format(username))