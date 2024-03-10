# CS-GY 6083 Spring 2024 Project

## Project Description
The project is to build an application that interfaces with a database to store and retrieve data. The application will be a simple command line interface that will allow the user to Create, Read, Update and Delete (CRUD) data. The data will be stored in a database and the application will use SQL to interact with the database.

## Project Requirements
The project will construct a database with 7 tables. The tables will be related to each other in a way that makes sense for the data. The application will allow the user to interact with the database by adding, retrieving, updating and deleting data. The application will also allow the user to query the database for specific data.

## Project Details
For my project I will construct a database to store information about record albums. The record album database will have a main table which lists the following features of a record album:

## Native Language
Python will be used to build the application and the database will be a MySQL database. The application will use the mysql library to interact with the database.

For security purposes, the password for the DB will be stored as an environment variable.

## Project Structure
The project will be structured as follows:
- ER Diagram from Record Album Database
- DLL
- Python Scripts for utilities
- Python Classes for Business Object definitions
- UI Classes to interact with the user

## Database Schema


### Entity Relationship Diagram
```mermaid
erDiagram

    RECORD_ARTISTS {
        artist_id int PK
        artist_name varchar(255)
    }
    GROUP_MEMBERS {
        member_id int
        member_name varchar(255)
    }
    ARTIST_TO_MEMBERS {
        member_id int FK
        artist_id int FK
        member_from_date date
        member_to_date date
    }
    RECORD_TRACKS {
        track_id int PK
        track_name varchar(255)
        track_number int
        genre_id int FK
    }
    RECORD_GENRES {
        genre_id int
        genre_name varchar(255)
        genre_description varchar(255)
    }
    RECORD_LABELS {
        record_label_id int
        record_label_name varchar(255)
    }
    RECORD_ALBUMS {
        album_id int PK
        album_name varchar(255)
        album_release_date date
        artist_id int FK
        genre_id int FK
        record_label_id int
    }
    ALBUM_TO_TRACKS {
        album_track_id int
        album_id int
        track_id int
    }
    RECORD_SALES {
        sale_id int
        sale_album_id int
        sale_date date
        sale_quantity int
        unit_sale_price decimal
    }

    RECORD_ALBUMS ||--|| RECORD_ARTISTS : "Artist"
    RECORD_ARTISTS ||--|| ARTIST_TO_MEMBERS : "Members"
    GROUP_MEMBERS ||--|| ARTIST_TO_MEMBERS : "Members"
    RECORD_ALBUMS ||--|| RECORD_GENRES : "Genre"
    RECORD_ALBUMS ||--|| RECORD_LABELS : "Record Label"
    RECORD_ALBUMS ||--|| ALBUM_TO_TRACKS : "Tracks"
    RECORD_ALBUMS ||--|| RECORD_SALES : "Sales"
    RECORD_TRACKS ||--|| RECORD_GENRES : "Genre"
    RECORD_TRACKS ||--|| ALBUM_TO_TRACKS : "Album Tracks"
    
```

## DDL for album_information database
```sql
CREATE DATABASE album_information;

USE album_information;

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

CREATE TABLE RECORD_ARTISTS (
    artist_id int NOT NULL AUTO_INCREMENT,
    artist_name varchar(255),
    PRIMARY KEY (artist_id)
);

CREATE TABLE GROUP_MEMBERS (
    member_id int NOT NULL AUTO_INCREMENT,
    member_name varchar(255),
    PRIMARY KEY (member_id)
);

CREATE TABLE MEMBERS_TO_ARTISTS (
    member_id int NOT NULL AUTO_INCREMENT,
    artist_id int,
    member_from_date date,
    member_to_date date,
    PRIMARY KEY (member_id),
    FOREIGN KEY (artist_id) REFERENCES RECORD_ARTISTS(artist_id)
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
```