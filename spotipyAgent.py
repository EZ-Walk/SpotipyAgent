import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import datetime as dt 
import os
import sys

def main(name, pID):
    """
    make a request to the Spotify web api using the playlist ID "pID" we recieved as input 
    """
    # this should start by getting the playlist's track's URIs with the endpoint below and saving that list of track_uris
    # GET https://api.spotify.com/v1/playlists/{playlist_id}/tracks
    # https://open.spotify.com/playlist/37i9dQZF1E37JNnK3FvjlV?si=m-9df_-HQlqrYHtfvx3NXA
    contents = []
    try:
        daily1Tracks = sp.playlist(pID, fields=['tracks'])

    except Exception as e:
        print('Error finding the playilist with the link: {}'.format(pID))
        print('Exiting!')
        sys.exit()
    
    for t in daily1Tracks['tracks']['items']: # Traverse to the 
        contents.append(t['track']['external_urls']['spotify'])
    # contents is now a populated list of 50 track URIs. Done

    # Create a new playlist named SavedDaily{N} or something like that. Use this endpoint to create a playlist
    # POST https://api.spotify.com/v1/users/{user_id}/playlists
    import datetime as dt
    g = 1
    newSavedName = '[[snaped]] {}'.format(name)
    savedFromName = sp.playlist(pID)['name']
    date = dt.date.today().strftime('%B %d, %Y')
    creationResp = sp.user_playlist_create('wakerXD', newSavedName, description='A snapshot of {} from {}'.format(savedFromName, date))
    savedDailyID = creationResp['id']

    # Next it should take this list of tracks found in the targeted DailyMix and add them to SavedDaily{N} with this endpoint
    # POST https://api.spotify.com/v1/playlists/{playlist_id}/tracks
    # This takes in a list of URIs to add
    sp.user_playlist_add_tracks('wakerXD', savedDailyID, contents)

def parse_args(args):

    a = [str(i) for i in args]

    return a


if __name__ == "__main__":
    a = parse_args(sys.argv)

    if a[1] == 'help' :
        print('Try: python3 spotipyAgent.py <name your playlist> <paste the link or URI>')
        sys.exit()
    
    elif len(a) != 3:
        print('Invalid number of arguments.  Usage: python3 spotipyAgent.py <newPlaylistName> <URL>')
        print('Exiting!')
        sys.exit()
    else:
        print('OK, creating the playlist "{}" based on the link you shared.'.format(str(a[1]).upper))

    os.environ['SPOTIPY_CLIENT_ID']='411ed1fc291749ccaf9523138836a2dd'
    os.environ['SPOTIPY_CLIENT_SECRET']='d5597fa540c84aa9ade5859bba91b681'
    os.environ['REDIRECT_URI']='http://trythis/callback'

    scopes = 'user-read-currently-playing user-library-read playlist-modify-public'
    token = util.prompt_for_user_token('wakerxd', scope=scopes, client_id='411ed1fc291749ccaf9523138836a2dd',client_secret='d5597fa540c84aa9ade5859bba91b681',redirect_uri='http://trythis/callback')
    
    if token:
        sp = spotipy.Spotify(auth=token)

        name = str(sys.argv[1])
        copyURL = str(sys.argv[2])
        pID = copyURL.split('/')[-1].split('?')[0]

        print('Prelims Complete!\nCreating Playlist: {}\nBased on URL: {}'.format(name, copyURL))

        main(name, pID)
    else:
        print('Couldn\'t get token for user')