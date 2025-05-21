from config import db
import config as cf

class Genre(db.Model):
    __tablename__ = 'Genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    playlists = db.relationship("Playlist", back_populates="genre", cascade='all, delete')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'\nid: {self.id}, Название: {self.name}'

class Playlist(db.Model):
    __tablename__ = 'Playlist'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    genreId = db.Column(db.Integer, db.ForeignKey('Genre.id'))

    genre = db.relationship("Genre", back_populates="playlists")
    tracks = db.relationship("Track", back_populates="playlist", cascade='all, delete')

    def __init__(self, id, name, genreId):
        self.id = id
        self.name = name
        self.genreId = genreId

    def __repr__(self):
        return f'\nid: {self.id}, Название: {self.name}, Жанр: {self.genreId}'

class Track(db.Model):
    __tablename__ = 'Track'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    danceability = db.Column(db.Float, nullable=False)
    releaseDate = db.Column(db.Date, nullable=False)
    playlistId = db.Column(db.String(50), db.ForeignKey('Playlist.id'))

    playlist = db.relationship("Playlist", back_populates="tracks")
    trackArtists = db.relationship("TrackArtist", back_populates="track", cascade='all, delete')

    def __init__(self, id, name, danceability, releaseDate, playlistId):
        self.id = id
        self.name = name
        self.danceability = danceability
        self.releaseDate = releaseDate
        self.playlistId = playlistId

    def __repr__(self):
        return f'\nid: {self.id}, Название: {self.name}, danceability: {self.danceability}, Дата: {self.releaseDate}, playlistId: {self.playlistId}'

class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    trackArtists = db.relationship("TrackArtist", back_populates="artist", cascade='all, delete')

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'\nid: {self.id}, Название: {self.name}'

class TrackArtist(db.Model):
    __tablename__ = 'TrackArtist'
    id = db.Column(db.Integer, primary_key=True)
    artistId = db.Column(db.String(50), db.ForeignKey('Artist.id'))
    trackId = db.Column(db.String(50), db.ForeignKey('Track.id'))

    track = db.relationship("Track", back_populates="trackArtists")
    artist = db.relationship("Artist", back_populates="trackArtists")

    def __init__(self, artistId, trackId):
        self.artistId = artistId
        self.trackId = trackId

    def __repr__(self):
        return f'\nid: {self.id}, artistId: {self.artistId}, trackId: {self.trackId}'


cf.app.app_context().push()
with cf.app.app_context():
    db.create_all()
