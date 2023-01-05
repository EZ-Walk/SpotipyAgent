from flask import Blueprint, current_app, jsonify
from flask.globals import request
from flask_restful import Api
from marshmallow import ValidationError
from spotagent.extensions import apispec
from spotagent.api.resources import UserResource, UserList
from spotagent.api.schemas import UserSchema

import spotipyAgent


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400

@blueprint.route('/clone', methods=['POST'])
def clone_playlist():
    print(request.form)
    return request.form
    formData = request.form

# def clone(name, pid):
#     """
#     make a request to the Spotify web api using the playlist ID "pID" we recieved as input 
#     """
#     # this should start by getting the playlist's track's URIs with the endpoint below and saving that list of track_uris
#     # GET https://api.spotify.com/v1/playlists/{playlist_id}/tracks
#     # https://open.spotify.com/playlist/37i9dQZF1E37JNnK3FvjlV?si=m-9df_-HQlqrYHtfvx3NXA
#     contents = []
#     try:
#         daily1Tracks = sp.playlist(pID, fields=['tracks'])

#     except Exception as e:
#         print('Error finding the playilist with the link: {}'.format(pID))
#         print('Exiting!')
#         sys.exit()
    
#     for t in daily1Tracks['tracks']['items']: # Traverse to the 
#         contents.append(t['track']['external_urls']['spotify'])
#     # contents is now a populated list of 50 track URIs. Done

#     # Create a new playlist named SavedDaily{N} or something like that. Use this endpoint to create a playlist
#     # POST https://api.spotify.com/v1/users/{user_id}/playlists
#     import datetime as dt
#     g = 1
#     newSavedName = '[[snaped]] {}'.format(name)
#     savedFromName = sp.playlist(pID)['name']
#     date = dt.date.today().strftime('%B %d, %Y')
#     creationResp = sp.user_playlist_create('wakerXD', newSavedName, description='A snapshot of {} from {}'.format(savedFromName, date))
#     savedDailyID = creationResp['id']

#     # Next it should take this list of tracks found in the targeted DailyMix and add them to SavedDaily{N} with this endpoint
#     # POST https://api.spotify.com/v1/playlists/{playlist_id}/tracks
#     # This takes in a list of URIs to add
#     sp.user_playlist_add_tracks('wakerXD', savedDailyID, contents)
