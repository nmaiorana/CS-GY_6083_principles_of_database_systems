# CS-GY 6083 Spring 2024 Project
* **Author**: [Nicola Maiorana]
* **Date**: [2024-03-17]
* **Email**: [nam10102@nyu.edu]
* **Class**: [CS-GY 6083]

## Project Description
The project is to build an application that interfaces with a database to store and retrieve data. The application will be a simple command line interface that will allow the user to Create, Read, Update and Delete (CRUD) data. The data will be stored in a database and the application will use SQL to interact with the database.

## Project Requirements
The project will construct a database with a minimum of 7 tables. The tables will be related to each other in a way that makes sense for the data. The application will allow the user to interact with the database by adding, retrieving, updating and deleting data. The application will also allow the user to query the database for specific data.

## Project Details
For this project I will construct a database using MySQL to store information about record album: the name of the album, the recording date, the artists behind the album (bands), the members of the recording group, the record label which produced the album, genre and sales information. This will utilize a 2-tier architecture using Python as the primary Language.

I will construct business object classes to represent the data in Python using data classes. To map these data classes to the MySQL db, I will use the MySQL Connect coupled with dataclasses to create my Business Objects. Lastly I will construct a series of UI classes to perform Create, Read, Update and Delete operations on one of the tables.

## Entity Relationship Diagram
```mermaid
erDiagram
    RECORD_ALBUMS |o--|| RECORD_ARTISTS : "Album Artist"
    RECORD_ALBUMS ||--o| RECORD_TRACKS : "Songs"

    RECORD_TRACKS |o--|| RECORD_GENRES : "Is of Genre"
    RECORD_ALBUMS |o--|| RECORD_GENRES : "Is of Genre"
    RECORD_ALBUMS |o--|| RECORD_LABELS : "Developed by"


    RECORD_ARTISTS ||--o| MEMBERS_TO_ARTIST : "Band Members"
    GROUP_MEMBERS ||--o| MEMBERS_TO_ARTIST : "Is Member of"
    RECORD_ALBUMS ||--o| RECORD_SALES : "Sales on"

    RECORD_ARTISTS {
        artist_id int PK
        artist_name varchar(255)
    }
    GROUP_MEMBERS {
        member_id int PK
        member_name varchar(255)
    }
    MEMBERS_TO_ARTIST {
        MEMBERS_TO_ARTIST_id int PK
        member_id int FK
        artist_id int FK
        member_from_date date
        member_to_date date
    }
    RECORD_TRACKS {
        track_id int PK
        album_id int FK
        track_number int
        track_name varchar(255)
        genre_id int FK
    }
    RECORD_GENRES {
        genre_id int PK
        genre_name varchar(255) "UNIQUE"
        genre_description varchar(255)
    }
    RECORD_LABELS {
        record_label_id int PK
        record_label_name varchar(255) "UNIQUE"
    }
    RECORD_ALBUMS {
        album_id int PK
        name varchar(255) "UNIQUE"
        release_date date
        artist_id int FK
        genre_id int FK
        record_label_id int
    }
    RECORD_SALES {
        sale_id int PK
        sale_album_id int FK
        sale_date date
        sale_quantity int
        unit_sale_price decimal
    }


    
```