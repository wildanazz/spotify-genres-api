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

@app.route('/send_top_genres_by_listen_count')
def send_top_genres_by_listen_count():
    # Get the token from the session
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))
    
    try:
        # Use the access token to create a Spotify instance
        sp = Spotify(auth=token_info['access_token'])
        
        # Fetch the user's recently played tracks (let's say we fetch the last 100 tracks)
        recent_tracks_res = sp.current_user_recently_played(limit=100)
        recent_tracks = recent_tracks_res['items']
        
        # Dictionary to count genres based on track plays
        genre_counts = {}
        
        # Iterate through the recent tracks
        for track_info in recent_tracks:
            track = track_info['track']
            artist = track['artists'][0]  # Get the first artist for simplicity
            
            # Fetch the artist's genres
            genres = artist['genres']
            
            # Update genre counts for each genre of the track
            for genre in genres:
                if genre in genre_counts:
                    genre_counts[genre] += 1
                else:
                    genre_counts[genre] = 1
        
        # Sort genres by the number of listens (highest first)
        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Prepare the genres list (sorted by listen count)
        genres_list = ",".join([genre for genre, count in sorted_genres])
        
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