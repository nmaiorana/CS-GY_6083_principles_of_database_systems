from tkinter import Tk
from tkinter import messagebox
from tkinter import OptionMenu
from tkinter import Button
from tkinter import Entry
from tkinter import Label
from tkinter import StringVar

from business_objects.record_album_sql import RecordAlbum
from business_objects.record_artists_sql import RecordArtist
from business_objects.record_genres_sql import RecordGenre
from business_objects.record_labels_sql import RecordLabel
from business_objects.record_tracks_sql import RecordTrack


class RecordAlbumUI:
    def __init__(self):
        self.optionMenu = None
        self.root = Tk()
        self.root.title('Record Album Manager')
        self.root.geometry('1000x400')
        self.root.mainloop()

    def create_widgets(self):
        pass

    def reset_window(self):
        pass

if __name__ == '__main__':
    RecordAlbumUI()
