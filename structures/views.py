from app import app
from flask import render_template
from structures.models import getDanceabilityStatsByGenre, getTopArtistsAboveAverage, getTrackCountGenre, getTracksDistributionByPlaylist, getTracksStatsByYear, get_all_tracks


@app.route('/')

def index():
    [tracksHead, tracksBody] = get_all_tracks()
    [artistCountHead, artistCountBody] = getTopArtistsAboveAverage()
    [dancebilityByGenreHead, dancebilityByGenreBody] = getDanceabilityStatsByGenre()
    [tracksByGenreHead, tracksByGenreBody] = getTrackCountGenre()
    [tracksDistributionByPlaylistHead, tracksDistributionByPlaylistBody] = getTracksDistributionByPlaylist()
    [tracksStatsByYearHead, tracksStatsByYearBody] = getTracksStatsByYear()


    html = render_template(
        'index.html',
        tracksHead = tracksHead,
        tracksBody = tracksBody,
        artistCountHead = artistCountHead, 
        artistCountBody = artistCountBody,
        dancebilityByGenreHead = dancebilityByGenreHead,
        dancebilityByGenreBody = dancebilityByGenreBody,
        tracksByGenreHead = tracksByGenreHead,
        tracksByGenreBody = tracksByGenreBody,
        tracksDistributionByPlaylistHead = tracksDistributionByPlaylistHead,
        tracksDistributionByPlaylistBody = tracksDistributionByPlaylistBody,
        tracksStatsByYearHead = tracksStatsByYearHead,
        tracksStatsByYearBody = tracksStatsByYearBody
    )

    return html