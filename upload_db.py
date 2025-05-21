from config import db
from models import Artist, Track, Genre, TrackArtist, Playlist
import csv
from datetime import datetime

def upload_genres():
    with open("data/data.csv", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        genres = set()
        for row in reader:
            genres.add(row['playlist_genre'])
        
        for genre_name in genres:
            exists = Genre.query.filter_by(name=genre_name).first()
            if not exists:
                new_genre = Genre(name=genre_name)
                db.session.add(new_genre)
        db.session.commit()

def upload_playlists():
    with open("data/data.csv", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        playlists = set()
        for row in reader:
            genre = Genre.query.filter_by(name=row['playlist_genre']).first()
            if genre:
                playlists.add((row['playlist_id'], row['playlist_name'], genre.id))
        
        for pl_id, pl_name, genre_id in playlists:
            if not Playlist.query.get(pl_id):
                new_playlist = Playlist(id=pl_id, name=pl_name, genreId=genre_id)
                db.session.add(new_playlist)
        db.session.commit()

def upload_artists():
    with open("data/data.csv", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        artists = set()
        for row in reader:
            for artist_name in row['track_artist'].split(', '):
                artist_id = artist_name.lower().replace(' ', '_')
                artists.add((artist_id, artist_name.strip()))
        
        for artist_id, artist_name in artists:
            if not Artist.query.get(artist_id):
                new_artist = Artist(id=artist_id, name=artist_name)
                db.session.add(new_artist)
        db.session.commit()

def upload_tracks():
    with open("data/data.csv", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not Track.query.get(row['track_id']):
                try:
                    release_date = datetime.strptime(row['track_album_release_date'], '%Y-%m-%d').date()
                except:
                    try:
                        release_date = datetime.strptime(row['track_album_release_date'][:4] + '-01-01', '%Y-%m-%d').date()
                    except:
                        release_date = datetime.now().date()
                
                new_track = Track(
                    id=row['track_id'],
                    name=row['track_name'],
                    danceability=float(row['danceability']),
                    releaseDate=release_date,
                    playlistId=row['playlist_id']
                )
                db.session.add(new_track)
        db.session.commit()

def upload_track_artists():
    with open("data/data.csv", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            track_id = row['track_id']
            for artist_name in row['track_artist'].split(', '):
                artist_id = artist_name.lower().replace(' ', '_')
                exists = db.session.query(TrackArtist).filter_by(
                    trackId=track_id,
                    artistId=artist_id
                ).first()
                if not exists:
                    new_relation = TrackArtist(
                        artistId=artist_id,
                        trackId=track_id
                    )
                    db.session.add(new_relation)
        db.session.commit()

# upload_genres()
# upload_playlists()
# upload_artists()
# upload_tracks()
# upload_track_artists()