# CS-GY 6083 Spring 2024 Project

## Project Description
The project is to build an application that interfaces with a database to store and retrieve data. The application will be a simple command line interface that will allow the user to Create, Read, Update and Delete (CRUD) data. The data will be stored in a database and the application will use SQL to interact with the database.

## Project Requirements
The project will construct a database with 7 tables. The tables will be related to each other in a way that makes sense for the data. The application will allow the user to interact with the database by adding, retrieving, updating and deleting data. The application will also allow the user to query the database for specific data.

Python will be used to build the application and the database will be a MySQL database. The application will use the mysql library to interact with the database.

For security purposes, the password for the DB will be stored as an environment variable.

## Project Structure
The project will be structured as follows:
- A main file that will contain the main logic of the application
  - A file that will contain the database schema
  - A file that will contain the database connection logic
  - A file that will contain the logic to interact with the database
  - A file that will contain the logic to interact with the user
  - A file that will contain the logic to handle the environment variables

## Database Schema
### Schema Name: album_information

The database will contain 7 tables. The tables will be related to each other in a way that makes sense for the data. The tables will be as follows:
- Table 1: record_albums
- Table 2: record_artists
- Table 3: record_tracks
- Table 4: record_genres
- Table 5: record_labels
- Table 6: record_producers
- Table 7: record_sales

### record_albums schema
- album_id: int
- album_name: varchar
- album_release_date: date
- album_artist_id: int
- album_label_id: int
- album_producer_id: int

### record_artists schema
- artist_id: int
- artist_name: varchar

### record_tracks schema
- track_id: int
- track_name: varchar
- track_album_id: int
- track_genre_id: int

### record_genres schema
- genre_id: int
- genre_name: varchar
- genre_description: varchar

### record_labels schema
- label_id: int
- label_name: varchar
- label_description: varchar

### record_producers schema
- producer_id: int
- producer_name: varchar

### record_sales schema
- sale_id: int
- sale_album_id: int
- sale_date: date
- sale_quantity: int
- sale_price: decimal

### Entity Relationship Diagram
```mermaid
erDiagram
    record_albums {
        album_id int
        album_name varchar
        album_release_date date
        album_artist_id int
        album_label_id int
        album_producer_id int
    }
    record_artists {
        artist_id int
        artist_name varchar
    }
    record_tracks {
        track_id int
        track_name varchar
        track_album_id int
        track_genre_id int
    }
    record_genres {
        genre_id int
        genre_name varchar
        genre_description varchar
    }
    record_labels {
        label_id int
        label_name varchar
        label_description varchar
    }
    record_producers {
        producer_id int
        producer_name varchar
    }
    record_sales {
        sale_id int
        sale_album_id int
        sale_date date
        sale_quantity int
        sale_price decimal
    }
    record_albums ||--|| record_artists : "album_artist_id"
    record_albums ||--|| record_labels : "album_label_id"
    record_albums ||--|| record_producers : "album_producer_id"
    record_tracks ||--|| record_albums : "track_album_id"
    record_tracks ||--|| record_genres : "track_genre_id"
    record_sales ||--|| record_albums : "sale_album_id"
```