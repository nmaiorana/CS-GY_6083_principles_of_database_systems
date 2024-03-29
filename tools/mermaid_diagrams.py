import base64
from IPython.display import Image, display


def mm_ink(graphbytes):
    """Given a bytes object holding a Mermaid-format graph, return a URL that will generate the image."""
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    return "https://mermaid.ink/img/" + base64_string


def mm_display(graphbytes):
    """Given a bytes object holding a Mermaid-format graph, display it."""
    display(Image(url=mm_ink(graphbytes)))


def mm(graph):
    """Given a string containing a Mermaid-format graph, display it."""
    graphbytes = graph.encode("ascii")
    mm_display(graphbytes)


def mm_link(graph):
    """Given a string containing a Mermaid-format graph, return URL for display."""
    graphbytes = graph.encode("ascii")
    return mm_ink(graphbytes)


def mm_path(path):
    """Given a path to a file containing a Mermaid-format graph, display it"""
    with open(path, 'rb') as f:
        graphbytes = f.read()
    mm_display(graphbytes)

er_diargram = """
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
"""