import os
from flask import Flask, redirect, request, session, url_for, jsonify
from flask_cors import CORS
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Set up your Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://wildanazz.github.io"}}) # Allow cross-origin requests
app.secret_key = os.urandom(24)  # Secret key for session
app.config['SESSION_COOKIE_NAME'] = 'my_flask_app_session'

# Set the scope to request access to the user's top artists, genres, and playlists
SCOPE = 'user-top-read user-library-read'

# Create SpotifyOAuth instance
sp_oauth = SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),
                         client_secret=os.getenv('CLIENT_SECRET'),
                         redirect_uri=os.getenv('REDIRECT_URI'),
                         scope=SCOPE)

@app.route('/login')
def login():
    # Redirect the user to Spotify for authentication
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Spotify redirects back to this URL with the authorization code
    token_info = sp_oauth.get_access_token(request.args['code'])
    session['token_info'] = token_info
    
    # After getting the token, redirect to the frontend and pass the token in the query string
    return redirect(url_for('send_top_genres'))

@app.route('/send_top_genres')
def send_top_genres():
    # Get the token from the session
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))
    
    # Use the access token to create a Spotify instance
    sp = Spotify(auth=token_info['access_token'])
    
    # Get the user's top artists (50 at a time)
    top_artists_res1 = sp.current_user_top_artists(limit=50, offset=0, time_range="medium_term")
    top_artists_res2 = sp.current_user_top_artists(limit=50, offset=50, time_range="medium_term")
    
    # Combine the results of the two API calls
    top_artists = top_artists_res1['items']
    if len(top_artists_res2['items']) > 0:
        top_artists += top_artists_res2['items']
    
    # Check if there are any top artists
    if not top_artists:
        # Handle case where the user doesn't have top artists (new user)
        genres_list = ""
    else:
        # Extract genres from top artists
        genres = set()
        for artist in top_artists:
            genres.update(artist['genres'])
        
        # Prepare the genres list as a comma-separated string
        genres_list = ",".join(genres)
    
    session.pop('token_info', None)
    
    # Redirect to the frontend with genres data in the URL (query params)
    return redirect(f"https://wildanazz.github.io/d3-spotify-genres/?genres={genres_list}")

if __name__ == '__main__':
    app.run(debug=True)
