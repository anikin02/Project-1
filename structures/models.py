from config import db 
from models import Artist, Track, TrackArtist, Genre, Playlist
from sqlalchemy import func

def getTracksDistributionByPlaylist():
    result = (db.session.query(
        Playlist.name.label("Плейлист"),
        Genre.name.label("Жанр"),
        func.count(Track.id).label("Количество треков"),
        func.round(func.avg(Track.danceability), 2).label("Средняя танцевальность")
    )
    .join(Playlist.genre)
    .join(Playlist.tracks)
    .group_by(Playlist.name, Genre.name)
    .order_by(func.count(Track.id).desc())
    )
    return [result.statement.columns.keys(), result.all()]

def getTopArtistsAboveAverage():
    avg_subquery = db.session.query(
        func.count(TrackArtist.trackId).label('avg_count')).group_by(TrackArtist.artistId).subquery()
    
    result = db.session.query(
        Artist.name.label("Артист"),
        func.count(TrackArtist.trackId).label("Количество треков")
    ).join(TrackArtist).group_by(Artist.id).having(
        func.count(TrackArtist.trackId) > db.session.query(
            func.avg(avg_subquery.c.avg_count)
        ).scalar_subquery()
    ).order_by(func.count(TrackArtist.trackId).desc())
    
    return [result.statement.columns.keys(), result.all()]

def getTracksStatsByYear():
    result = (db.session.query(
        func.extract('year', Track.releaseDate).label("Год"),
        func.count(Track.id).label("Количество треков"),
        func.round(func.avg(Track.danceability), 2).label("Средняя танцевальность")
    )
    .group_by(func.extract('year', Track.releaseDate))
    .order_by(func.extract('year', Track.releaseDate).desc())
    )
    return [result.statement.columns.keys(), result.all()]

def getTrackCountGenre():
    result = (db.session.query(
        Genre.name.label("Жанр"),
        func.count(Track.id).label("Количество треков")
    )
    .join(Genre.playlists)
    .join(Playlist.tracks)
    .group_by(Genre.name)
    .order_by(func.count(Track.id).desc())
    )
    return [result.statement.columns.keys(), result.all()]

def getDanceabilityStatsByGenre():
    result = (db.session.query(
        Genre.name.label("Жанр"),
        func.max(Track.danceability).label("Максимальная танцевальность"),
        func.min(Track.danceability).label("Минимальная танцевальность"),
        func.round(func.avg(Track.danceability), 2).label("Средняя танцевальность")
    )
    .join(Genre.playlists)
    .join(Playlist.tracks)
    .group_by(Genre.name)
    .order_by(Genre.name.asc())
    )
    return [result.statement.columns.keys(), result.all()]

def get_all_tracks():
    query = (
        db.session.query(
            Track.name.label("Название трека"),
            Playlist.name.label("Плейлист"),
            Genre.name.label("Жанр"),
            func.group_concat(Artist.name, ", ").label("Все артисты"),
            Track.danceability.label("Танцевальность"),
            Track.releaseDate.label("Дата релиза"),
        )
        .join(Track.playlist)
        .join(Playlist.genre)
        .join(Track.trackArtists)
        .join(TrackArtist.artist)
        .group_by(Track.id, Playlist.name, Genre.name)
    )
    return [query.statement.columns.keys(), query.all()]