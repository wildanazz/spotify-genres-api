# Spotify Genres API

Spotify Genres API is a server application designed to support the [d3-spotify-genres](https://github.com/wildanazz/d3-spotify-genres) project. 
It provides endpoints to interact with Spotify's Web API, enabling the retrieval of genre-related data for visualization purposes.

## Features

- **Authentication**: Facilitates user authentication with Spotify to access personalized data.
- **Genre Data Retrieval**: Fetches genre information associated with the user's top artists.
- **Data Formatting**: Processes and formats data to be compatible with D3.js visualizations.

## Prerequisites

Before running the application, ensure you have the following:

- **Python 3.x**: The application is built using Python.
- **Spotify Developer Account**: Necessary to obtain API credentials.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/wildanazz/spotify-genres-api.git
   cd spotify-genres-api
   ```

2. **Set up a virtual environment** (optional but recommended):

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   Create a `.env` file in the project root and add your Spotify API credentials:

   ```
   CLIENT_ID='your_spotify_client_id'
   CLIENT_SECRET='your_spotify_client_secret'
   REDIRECT_URI='http://localhost:5000/callback'
   ```

   Replace `'your_spotify_client_id'` and `'your_spotify_client_secret'` with your actual Spotify API credentials.

## Usage

1. **Run the application**:

   ```bash
   python app.py
   ```

2. **Access the application**:

   Open your web browser and navigate to `http://localhost:5000/login` to authenticate with your Spotify account.

3. **Retrieve genre data**:

   After authentication, the server will fetch and process your top artists' genre information, making it available for visualization.

## Todo

- Develop more endpoints.
- Create a workflow for deployment.

## License

This project is licensed under the MIT License. See the [LICENSE.md](https://github.com/wildanazz/spotify-genres-api/blob/main/LICENSE.md) file for details.
