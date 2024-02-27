/******************************************************************************
  This script creates a pre-populated database for the album information
*******************************************************************************/

DROP DATABASE IF EXISTS album_information;
CREATE DATABASE album_information;
USE album_information;

CREATE TABLE record_albums (
    album_id int NOT NULL AUTO_INCREMENT,
    album_name varchar(255) NOT NULL,
    album_release_date date NOT NULL,
    PRIMARY KEY (album_id)
);

CREATE TABLE record_artists (
    artist_id int NOT NULL AUTO_INCREMENT,
    artist_name varchar(255) NOT NULL,
    PRIMARY KEY (artist_id)
);

CREATE TABLE record_tracks (
    track_id int NOT NULL AUTO_INCREMENT,
    track_name varchar(255) NOT NULL,
    genre_id int NOT NULL,
    PRIMARY KEY (track_id)
);

CREATE TABLE record_genres (
    genre_id int NOT NULL AUTO_INCREMENT,
    genre_name varchar(255) NOT NULL,
    genre_description varchar(512) NOT NULL,
    PRIMARY KEY (genre_id)
);

CREATE TABLE album_to_artists (
    album_artist_id int NOT NULL AUTO_INCREMENT,
    album_id int NOT NULL,
    artist_id int NOT NULL,
    PRIMARY KEY (album_artist_id),
    FOREIGN KEY (album_id) REFERENCES record_albums(album_id),
    FOREIGN KEY (artist_id) REFERENCES record_artists(artist_id)
);

CREATE TABLE album_to_tracks (
    album_track_id int NOT NULL AUTO_INCREMENT,
    album_id int NOT NULL,
    track_id int NOT NULL,
    track_number int NOT NULL,
    PRIMARY KEY (album_track_id),
    FOREIGN KEY (album_id) REFERENCES record_albums(album_id),
    FOREIGN KEY (track_id) REFERENCES record_tracks(track_id)
);

CREATE TABLE record_sales (
    sale_id int NOT NULL AUTO_INCREMENT,
    sale_album_id int NOT NULL,
    sale_date date NOT NULL,
    sale_quantity int NOT NULL,
    sale_price decimal(10,2) NOT NULL,
    PRIMARY KEY (sale_id),
    FOREIGN KEY (sale_album_id) REFERENCES record_albums(album_id)
);

CREATE VIEW album_information AS
    SELECT
        record_albums.album_name,
        record_albums.album_release_date,
        record_artists.artist_name,
        record_genres.genre_name,
        album_to_tracks.track_number,
        record_tracks.track_name

    FROM
        record_albums
    JOIN
        album_to_artists ON record_albums.album_id = album_to_artists.album_id
    JOIN
        record_artists ON album_to_artists.artist_id = record_artists.artist_id
    JOIN
        album_to_tracks ON record_albums.album_id = album_to_tracks.album_id
    JOIN
        record_tracks ON album_to_tracks.track_id = record_tracks.track_id
    JOIN
        record_genres ON record_tracks.genre_id = record_genres.genre_id;

INSERT INTO record_albums (album_name, album_release_date) VALUES
    ('The Dark Side of the Moon', '1973-03-01');

INSERT INTO record_artists (artist_name) VALUES
    ('Pink Floyd');

INSERT INTO record_genres (genre_name, genre_description) VALUES
    ('Rock', 'Rock music');

INSERT INTO record_tracks (track_name, genre_id) VALUES
    ('Speak to Me', (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('Breathe', (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('On the Run', (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('Time', (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('The Great Gig in the Sky', (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('Money', (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('Us and Them', (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('Any Colour You Like', (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('Brain Damage', (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock')),
    ('Eclipse', (SELECT genre_id FROM record_genres WHERE genre_name = 'Rock'));

INSERT INTO album_to_artists (album_id, artist_id) VALUES
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT artist_id FROM record_artists WHERE artist_name = 'Pink Floyd'));

INSERT INTO album_to_tracks (album_id, track_id, track_number) VALUES
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'Speak to Me'), 1),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'Breathe'), 2),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'On the Run'), 3),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'Time'), 4),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'The Great Gig in the Sky'), 5),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'Money'), 6),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'Us and Them'), 7),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'Any Colour You Like'), 8),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'Brain Damage'), 9),
    ((SELECT album_id FROM record_albums WHERE album_name = 'The Dark Side of the Moon'), (SELECT track_id FROM record_tracks WHERE track_name = 'Eclipse'), 10);

