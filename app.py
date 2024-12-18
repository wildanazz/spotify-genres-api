import os
from flask import Flask, redirect, request, session, url_for, jsonify
from flask_cors import CORS
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Set up your Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://wildanazz.github.io"}})  # Allow cross-origin requests
app.secret_key = os.urandom(24)  # Secret key for session
app.config['SESSION_COOKIE_NAME'] = 'spotify_app_session'

# Set the scope to request access to the user's top artists, genres, and playlists
SCOPE = 'user-top-read user-library-read'

# Create SpotifyOAuth instance
sp_oauth = SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),
                         client_secret=os.getenv('CLIENT_SECRET'),
                         redirect_uri=os.getenv('REDIRECT_URI'),
                         scope=SCOPE)

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Empty response with no content (status code 204)

@app.route('/login')
def login():
    # Redirect the user to Spotify for authentication
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    try:
        # Spotify redirects back to this URL with the authorization code
        token_info = sp_oauth.get_access_token(request.args['code'])
        session['token_info'] = token_info
        # After getting the token, redirect to the frontend and pass the token in the query string
        return redirect(url_for('send_top_genres'))
    except Exception as e:
        # Handle the error if authentication fails
        return jsonify({"error": str(e)}), 400

@app.route('/send_top_genres')
def send_top_genres():
    # Get the token from the session
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))
    
    try:
        # Use the access token to create a Spotify instance
        sp = Spotify(auth=token_info['access_token'])
        
        # Get the user's top artists (50 at a time)
        top_artists_res1 = sp.current_user_top_artists(limit=50, offset=0, time_range="medium_term")
        top_artists_res2 = sp.current_user_top_artists(limit=50, offset=50, time_range="medium_term")
        top_artists = top_artists_res1['items'] + top_artists_res2['items']
        
        # Extract genres from top artists
        genres = set()
        for artist in top_artists:
            genres.update(artist['genres'])
        
        # Prepare the genres list as a comma-separated string
        genres_list = ",".join(genres)

        # Optionally log the genres list for debugging
        print(genres_list)

        # Clear session after sending the genres
        session.clear()

        # Redirect to the frontend with genres data in the URL (query params)
        return redirect(f"https://wildanazz.github.io/d3-spotify-genres/?genres={genres_list}")
    
    except Exception as e:
        # Handle the error if Spotify API request fails
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)