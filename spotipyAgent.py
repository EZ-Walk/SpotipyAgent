import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util
import datetime as dt 
import os
import sys

def clone_from_url(name, pID):
    """
    make a request to the Spotify web api using the playlist ID "pID" we recieved as input 
    """
    # this should start by getting the playlist's track's URIs with the endpoint below and saving that list of track_uris
    # GET https://api.spotify.com/v1/playlists/{playlist_id}/tracks
    # https://open.spotify.com/playlist/37i9dQZF1E37JNnK3FvjlV?si=m-9df_-HQlqrYHtfvx3NXA
    contents = []
    try:
        daily1Tracks = client.playlist(pID, fields=['tracks'])

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
    newSavedName = u'{}'.format(name)
    savedFromName = client.playlist(pID)['name']
    date = dt.date.today().strftime('%B %d, %Y')
    creationResp = client.user_playlist_create('wakerXD', newSavedName, description='A snapshot of {} from {}'.format(savedFromName, date))
    savedDailyID = creationResp['id']

    # Next it should take this list of tracks found in the targeted DailyMix and add them to SavedDaily{N} with this endpoint
    # POST https://api.spotify.com/v1/playlists/{playlist_id}/tracks
    # This takes in a list of URIs to add
    client.user_playlist_add_tracks('wakerXD', savedDailyID, contents)

def parse_args(args):

    a = [str(i) for i in args]

    return a

def get_client_for_user(user=None):
    
    # Create an Oauth object
    oAuth = spotipy.oauth2.SpotifyOAuth(username=user,
                         scope=scopes.split(' '),
                         client_id=os.environ['SPOTIPY_CLIENT_ID'],
                         client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
                         redirect_uri=os.environ['REDIRECT_URI'],
                         state='ape'
                         )
    
    # Attatche the oauth object to a spotify API client
    client = spotipy.Spotify(auth_manager=oAuth)
    
    # If this user is known to us, validate the token and return the client
    try: 
        client.auth_manager.get_cached_token().get('refresh_token')
        client.auth_manager.refresh_access_token(client.auth_manager.get_cached_token().get('refresh_token'))
        
    except spotipy.oauth2.SpotifyOauthError as e:
        if e.error == 'invalid_client':
            print('New user "{}" requested'.format(user))
            # TODO: function to authenticate a new user
            client = authenticate_new_user(client)
    except Exception as e:
        print('failed to get client for user', e)
        
    
    return client

def authenticate_new_user(client):
    
    auth_code = client.auth_manager.get_auth_response()
    
    access_token = client.auth_manager.get_access_token(code=auth_code, check_cache=False)
    
    if access_token.get('refresh_token'):
        client.auth_manager.refresh_access_token(access_token.get('refresh_token'))
    else:
        print('Failed to get access token for new user')    
        
    return client

if __name__ == "__main__":
    a = parse_args(sys.argv)

    if a[1] == 'help' :
        print('Try: python3 spotipyAgent.py <name your playlist> <paste the link or URI>')
        sys.exit()
    
    # Ensure 3 arguments were passed, ie: filename, newPlaylistName, URL 
    elif len(a) != 3:
        print('Invalid number of arguments.  Usage: python3 spotipyAgent.py <newPlaylistName> <URL>')
        print('Exiting!')
        sys.exit()
    else:
        print('OK, creating the playlist "{}" based on the link you shared.'.format(str(a[1])))

    # Uses SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI to create an authenticated API client
    os.environ['SPOTIPY_CLIENT_ID']='acbdb84970564d238b485bd68b0f85bd'
    os.environ['SPOTIPY_CLIENT_SECRET']=''
    os.environ['REDIRECT_URI']='http://spotifyagent.com/callback'

    scopes = 'user-read-currently-playing user-library-read playlist-modify-public'
    
    # Deprecated Authentication item
    # token = util.prompt_for_user_token('wakerxd', scope=scopes, client_id='411ed1fc291749ccaf9523138836a2dd',client_secret='d5597fa540c84aa9ade5859bba91b681',redirect_uri='http://trythis/callback')
    # New Auth item
    client = get_client_for_user('wakerXD')
    
    if client:

        name = str(sys.argv[1])
        copyURL = str(sys.argv[2])
        pID = copyURL.split('/')[-1].split('?')[0]

        print('Prelims Complete!\nCreating Playlist: {}\nBased on URL: {}'.format(name, copyURL))

        clone_from_url(name, pID)
    else:
        print('Couldn\'t get token for user')