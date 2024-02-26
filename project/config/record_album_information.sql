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
    track_genre_id int NOT NULL,
    PRIMARY KEY (track_id)
);

CREATE TABLE record_genres (
    genre_id int NOT NULL AUTO_INCREMENT,
    genre_name varchar(255) NOT NULL,
    genre_description varchar(255) NOT NULL,
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