# Create a form to add a new album to the record_album table

# Import the necessary modules
import album_information_connect as aic
import mysql.connector
from mysql.connector import errorcode
import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Get the password from the environment

cnx = aic.connect()

def register_album():
    # Get the values from the form
    album_name = album_name_entry.get()
    artist = artist_entry.get()
    release_date = release_date_entry.get()
    number_of_tracks = number_of_tracks_entry.get()
    record_label = record_label_entry.get()
    genre = genre_entry.get()

    # Create a cursor object
    cursor = cnx.cursor()

    # Create a query
    query = 'insert into album_information (album_name, artist, release_date, number_of_tracks, record_label, genre) values (%s, %s, %s, %s, %s, %s)'

    # Execute the query
    cursor.execute(query, (album_name, artist, release_date, number_of_tracks, record_label, genre))

    # Commit the changes
    cnx.commit()

    # Close the cursor
    cursor.close()

    # Close the connection
    cnx.close()

    # Show a message box
    messagebox.showinfo('Album Information', 'Album information has been added to the database')

    # Clear the form
    album_name_entry.delete(0, END)
    artist_entry.delete(0, END)
    release_date_entry.delete(0, END)
    number_of_tracks_entry.delete(0, END)
    record_label_entry.delete(0, END)
    genre_entry.delete(0, END)

    # Close the window
    album_entry_window.destroy()


# Create a window object
album_entry_window = Tk()

# Set the window title
album_entry_window.title('Add Album')

# Set the window size
album_entry_window.geometry('400x400')

# Create a frame
album_entry_frame = Frame(album_entry_window)

# Pack the frame
album_entry_frame.pack()

# Create a label for the album name
album_name_label = Label(album_entry_frame, text='Album Name')

# Pack the label
album_name_label.pack()

# Create a text entry for the album name
album_name_entry = Entry(album_entry_frame)

# Pack the text entry
album_name_entry.pack()

# Create a label for the artist
artist_label = Label(album_entry_frame, text='Artist')

# Pack the label
artist_label.pack()

# Create a text entry for the artist
artist_entry = Entry(album_entry_frame)

# Pack the text entry
artist_entry.pack()

# Create a label for the release date
release_date_label = Label(album_entry_frame, text='Release Date')

# Pack the label
release_date_label.pack()

# Create a text entry for the release date
release_date_entry = Entry(album_entry_frame)

# Pack the text entry
release_date_entry.pack()

# Create a label for the number of tracks
number_of_tracks_label = Label(album_entry_frame, text='Number of Tracks')

# Pack the label
number_of_tracks_label.pack()

# Create a text entry for the number of tracks
number_of_tracks_entry = Entry(album_entry_frame)

# Pack the text entry
number_of_tracks_entry.pack()

# Create a label for the record label
record_label_label = Label(album_entry_frame, text='Record Label')

# Pack the label
record_label_label.pack()

# Create a text entry for the record label
record_label_entry = Entry(album_entry_frame)

# Pack the text entry
record_label_entry.pack()

# Create a label for the genre
genre_label = Label(album_entry_frame, text='Genre')

# Pack the label
genre_label.pack()

# Create a text entry for the genre
genre_entry = Entry(album_entry_frame)

# Pack the text entry
genre_entry.pack()

register_button = Button(album_entry_frame, text='Register', command=register_album)
register_button.pack()

album_entry_window.mainloop()

