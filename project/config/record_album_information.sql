/******************************************************************************
  This script creates a pre-populated database for the album information
*******************************************************************************/

DROP DATABASE IF EXISTS album_information;

CREATE DATABASE album_information;

USE album_information;

CREATE TABLE RECORD_ARTISTS (
    artist_id int NOT NULL AUTO_INCREMENT,
    artist_name varchar(255),
    PRIMARY KEY (artist_id)
);

CREATE TABLE RECORD_TRACKS (
    track_id int NOT NULL AUTO_INCREMENT,
    track_name varchar(255),
    track_number int,
    genre_id int,
    PRIMARY KEY (track_id)
);

CREATE TABLE RECORD_GENRES (
    genre_id int NOT NULL AUTO_INCREMENT,
    genre_name varchar(255),
    genre_description varchar(255),
    PRIMARY KEY (genre_id)
);

CREATE TABLE RECORD_LABELS (
    record_label_id int NOT NULL AUTO_INCREMENT,
    record_label_name varchar(255),
    PRIMARY KEY (record_label_id)
);

CREATE TABLE RECORD_ALBUMS (
    album_id int NOT NULL AUTO_INCREMENT,
    album_name varchar(255),
    album_release_date date,
    artist_id int,
    genre_id int,
    record_label_id int,
    PRIMARY KEY (album_id),
    FOREIGN KEY (artist_id) REFERENCES RECORD_ARTISTS(artist_id),
    FOREIGN KEY (genre_id) REFERENCES RECORD_GENRES(genre_id),
    FOREIGN KEY (record_label_id) REFERENCES RECORD_LABELS(record_label_id)
);

CREATE TABLE ALBUM_TO_TRACKS (
    album_track_id int NOT NULL AUTO_INCREMENT,
    album_id int,
    track_id int,
    PRIMARY KEY (album_track_id),
    FOREIGN KEY (album_id) REFERENCES RECORD_ALBUMS(album_id),
    FOREIGN KEY (track_id) REFERENCES RECORD_TRACKS(track_id)
);

CREATE TABLE RECORD_SALES (
    sale_id int NOT NULL AUTO_INCREMENT,
    album_id int,
    sale_date date,
    sale_quantity int,
    unit_sale_price decimal,
    PRIMARY KEY (sale_id),
    FOREIGN KEY (sale_id) REFERENCES RECORD_ALBUMS(album_id)
);

CREATE VIEW album_information AS
    SELECT
        RECORD_ALBUMS.album_name,
        RECORD_ARTISTS.artist_name,
        RECORD_GENRES.genre_name,
        RECORD_LABELS.record_label_name,
        RECORD_ALBUMS.album_release_date
    FROM
        RECORD_ALBUMS
    JOIN RECORD_ARTISTS ON RECORD_ALBUMS.artist_id = RECORD_ARTISTS.artist_id
    JOIN RECORD_LABELS ON RECORD_ALBUMS.record_label_id = RECORD_LABELS.record_label_id
    JOIN RECORD_GENRES ON RECORD_ALBUMS.genre_id = RECORD_GENRES.genre_id;

CREATE VIEW album_information_details AS
    SELECT
        RECORD_ALBUMS.album_name,

        RECORD_ARTISTS.artist_name,
        record_genres.genre_name,
        RECORD_TRACKS.track_number,
        RECORD_TRACKS.track_name,
        RECORD_ALBUMS.album_release_date

    FROM
        RECORD_ALBUMS
    JOIN RECORD_ARTISTS ON RECORD_ALBUMS.artist_id = RECORD_ARTISTS.artist_id
    JOIN RECORD_LABELS ON RECORD_ALBUMS.record_label_id = RECORD_LABELS.record_label_id
    JOIN ALBUM_TO_TRACKS ON RECORD_ALBUMS.album_id = ALBUM_TO_TRACKS.album_id
    JOIN RECORD_TRACKS ON ALBUM_TO_TRACKS.track_id = RECORD_TRACKS.track_id
    JOIN RECORD_GENRES ON RECORD_TRACKS.genre_id = RECORD_TRACKS.genre_id
ORDER BY
    RECORD_ALBUMS.album_name, RECORD_TRACKS.track_number;


INSERT INTO record_artists (artist_name) VALUES
    ('Pink Floyd');

INSERT INTO record_genres (genre_name, genre_description) VALUES
    ('Rock', 'Rock music');

INSERT INTO record_labels (record_label_name) VALUES
    ('Harvest Capitol Records');

INSERT INTO record_albums (album_name, album_release_date, artist_id, genre_id, record_label_id) VALUES
    ('The Dark Side of the Moon', '1973-03-01', (SELECT artist_id FROM record_artists WHERE artist_name = 'Pink Floyd'), (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock'), (SELECT record_label_id FROM record_labels WHERE record_label_name = 'Harvest Capitol Records'));

INSERT INTO record_tracks (track_name, track_number, genre_id) VALUES
    ('Speak to Me', 1, (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('Breathe (In the Air)', 2, (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('On the Run', 3, (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('Time', 4, (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('The Great Gig in the Sky', 5, (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('Money', 6, (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('Us and Them', 7, (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('Any Colour You Like', 8, (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('Brain Damage', 9, (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('Eclipse', 10, (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock'));


INSERT INTO album_to_tracks (album_id, track_id) VALUES
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'Speak to Me')),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'Breathe (In the Air)')),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'On the Run')),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'Time')),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'The Great Gig in the Sky')),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'Money')),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'Us and Them')),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'Any Colour You Like')),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'Brain Damage')),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'Eclipse'));


