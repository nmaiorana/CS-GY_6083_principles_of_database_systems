from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import OptionMenu
from tkinter import Button
from tkinter import Entry
from tkinter import Label
from tkinter import StringVar
from tkcalendar import Calendar

from business_objects.record_album_sql import RecordAlbum
from business_objects.record_artists_sql import RecordArtist
from business_objects.record_genres_sql import RecordGenre
from business_objects.record_labels_sql import RecordLabel
from business_objects.record_tracks_sql import RecordTrack
from ui_objects.record_album_tracks_ui import RecordTracksUI


class RecordAlbumUI:
    def __init__(self):
        self.album_summary = None
        self.album_view = None
        self.track_view = None
        self.albums = []
        self.tracks = []
        self.selected_album = None
        self.selected_track = None
        self.primary = Tk()
        self.primary.geometry("1000x400")
        self.primary.title("Record Album Manager")

        self.build_main_window()
        self.load_albums()
        self.primary.mainloop()

    def remove_albums(self):
        for item in self.album_view.get_children():
            self.album_view.delete(item)

    def load_albums(self):
        self.remove_albums()
        self.selected_album = None
        self.selected_track = None
        self.albums = RecordAlbum.read_all()
        index = 0
        for album in self.albums:
            self.album_view.insert("", "end", values=(album.album_id, album.album_name, album.release_date,
                                                      album.artist_name(), album.genre_name(),
                                                      album.record_label_name()), iid=index)
            index += 1

    def build_main_window(self):
        new_button = Button(self.primary, text="New Album", padx=2, pady=3, command=lambda: self.create_new_album())
        new_button.grid(row=0, column=0, sticky="w")

        edit_button = Button(self.primary, text="Edit Album", command=lambda: self.edit_selected_album())
        edit_button.grid(row=0, column=1, sticky="w")

        delete_button = Button(self.primary, text="Delete Album", command=lambda: self.delete_selected_album(self.primary))
        delete_button.grid(row=0, column=2, sticky="w")

        self.album_view = ttk.Treeview(self.primary, columns=(
            "album_id", "album_name", "release_date", "artist_name", "gener_name", "record_label_name"),
                                       show="headings",
                                       height="10")
        self.album_view.grid(row=1, column=0, rowspan=10, columnspan=6)
        self.album_view.heading("album_id", text="Album ID", anchor="w")
        self.album_view.heading("album_name", text="Album Name", anchor="center")
        self.album_view.heading("release_date", text="Release Date", anchor="center")
        self.album_view.heading("artist_name", text="Artist", anchor="center")
        self.album_view.heading("gener_name", text="Genre", anchor="center")
        self.album_view.heading("record_label_name", text="Label", anchor="center")

        self.album_view.column("album_id", width=100)
        self.album_view.column("album_name", width=300)
        self.album_view.column("release_date", width=100)
        self.album_view.column("artist_name", width=200)
        self.album_view.column("gener_name", width=100)
        self.album_view.column("record_label_name", width=200)

        self.primary.bind("<FocusIn>", self.handle_primary_focus)

    def handle_primary_focus(self, event):
        self.load_albums()

    def create_new_album(self):
        self.selected_album = None
        self.selected_track = None
        self.edit_album()

    def edit_selected_album(self):
        if self.album_view.selection() is None or len(self.album_view.selection()) == 0:
            messagebox.showerror("No Selection", "Please select an album to edit!")
            return
        selected_item = int(self.album_view.selection()[0])
        self.selected_album = self.albums[selected_item]
        self.edit_album()

    def delete_selected_album(self, child):
        if self.album_view.selection() is None or len(self.album_view.selection()) == 0:
            messagebox.showerror("No Selection", "Please select an album to delete!")
            return
        selected_item = int(self.album_view.selection()[0])
        self.selected_album = self.albums[selected_item]
        self.delete_album()

    def edit_album(self):
        child = Toplevel(self.primary)
        artist_selected = StringVar()
        genre_selected = StringVar()
        record_label_selected = StringVar()
        if self.selected_album is None:
            frame_title = "New Album"
            artist_selected.set("Select Artist")
            genre_selected.set("Select Genre")
            record_label_selected.set("Select Record Label")
        else:
            frame_title = "Edit Album"
            artist_selected.set(self.selected_album.artist_name())
            genre_selected.set(self.selected_album.genre_name())
            record_label_selected.set(self.selected_album.record_label_name())

        child.title(frame_title)
        child.geometry("700x800")
        child.grab_set()

        load_form = True
        label_width = 20
        input_width = 60
        button_width = 10
        input_frame = LabelFrame(child, text="Enter new album information", padx=5, pady=5)

        input_frame.grid(row=0, rowspan=6, column=0)

        album_name_label = Label(input_frame, text="Album Name", width=label_width, height=2, anchor="w",
                                 relief="ridge")
        release_date_label = Label(input_frame, text="Release Date", width=label_width, height=2, anchor="w",
                                   relief="ridge")
        artist_label = Label(input_frame, text="Artist", width=label_width, height=2, anchor="w", relief="ridge")
        genre_label = Label(input_frame, text="Genre", width=label_width, height=2, anchor="w", relief="ridge")
        record_label_label = Label(input_frame, text="Record Label", width=label_width, height=2, anchor="w",
                                   relief="ridge")

        album_name_label.grid(row=0, column=0, padx=1, pady=0)
        release_date_label.grid(row=1, column=0, padx=1, pady=0)
        artist_label.grid(row=2, column=0, padx=1, pady=0)
        genre_label.grid(row=3, column=0, padx=1, pady=0)
        record_label_label.grid(row=4, column=0, padx=1, pady=0)

        album_name = StringVar()
        release_date = StringVar()
        artist_name = StringVar()
        record_label_name = StringVar()

        album_name_entry = Entry(input_frame, textvariable=album_name, width=input_width)
        release_date_entry = Calendar(input_frame, date_pattern="YYYY-MM-DD")
        # release_date_entry = Entry(input_frame, textvariable=release_date, width=input_width)
        artist_option_menu = OptionMenu(input_frame,
                                        artist_selected,
                                        *[artist.artist_name for artist in RecordArtist.read_all()])
        artist_option_menu.config(width=input_width)
        genre_option_menu = OptionMenu(input_frame,
                                       genre_selected,
                                       *[genre.genre_name for genre in RecordGenre.read_all()])
        genre_option_menu.config(width=input_width)
        record_label_option_menu = OptionMenu(input_frame,
                                              record_label_selected,
                                              *[record_label.record_label_name for record_label in
                                                RecordLabel.read_all()])
        record_label_option_menu.config(width=input_width)

        album_name_entry.grid(row=0, column=1, padx=1, pady=0)
        release_date_entry.grid(row=1, column=1, padx=1, pady=0)
        artist_option_menu.grid(row=2, column=1, padx=1, pady=0)
        genre_option_menu.grid(row=3, column=1, padx=1, pady=0)
        record_label_option_menu.grid(row=4, column=1, padx=1, pady=0)

        if self.selected_album is not None:
            album_name.set(self.selected_album.album_name)
            release_date_entry.selection_set(self.selected_album.release_date)
            artist_name.set(self.selected_album.artist_name())
            genre_selected.set(self.selected_album.genre_name())
            record_label_name.set(self.selected_album.record_label_name())
            update_album_button = Button(input_frame, text="Update",
                                         command=lambda: self.update_album(child,
                                                                           album_name.get(),
                                                                           release_date_entry.get_date(),
                                                                           artist_selected.get(),
                                                                           genre_selected.get(),
                                                                           record_label_selected.get()))
            update_album_button.config(width=button_width)
            add_track_button = Button(input_frame, text="Tracks", command=lambda: RecordTracksUI(child, self.selected_album))
            add_track_button.config(width=button_width)
            update_album_button.grid(row=5, column=0, padx=0, pady=1)
            add_track_button.grid(row=5, column=1, padx=0, pady=1)
        else:
            add_album_button = Button(input_frame, text="Add",
                                      command=lambda: self.create_album(child,
                                                                        album_name.get(),
                                                                        release_date_entry.get_date(),
                                                                        artist_selected.get(),
                                                                        genre_selected.get(),
                                                                        record_label_selected.get()))
            add_album_button.config(width=button_width)
            add_album_button.grid(row=5, column=0, padx=0, pady=1)

        cancel_button = Button(input_frame, text="Cancel", command=lambda: self.cancel_album(child))
        cancel_button.config(width=button_width)
        cancel_button.grid(row=5, column=2, padx=0, pady=1)

        self.album_summary = Text(child, height=20, width=60)
        self.album_summary.grid(row=6, column=0, padx=0, pady=1)
        self.update_album_summary()

        child.bind("<FocusIn>", self.handle_edit_album_focus)

        load_form = False

    def handle_edit_album_focus(self, event):
        self.update_album_summary()

    def update_album_summary(self):
        self.album_summary.config(state=NORMAL)
        self.album_summary.delete(1.0, END)
        if self.selected_album is not None:
            self.album_summary.insert(INSERT, self.selected_album.summary())
        self.album_summary.config(state=DISABLED)

    def create_album(self, child, album_name, release_date, artist_name, genre_name, record_label_name):
        if album_name == "" or album_name is None:
            messagebox.showerror("Missing Field", "Please enter an album name!")
            return
        if release_date == "" or release_date is None:
            messagebox.showerror("Missing Field", "Please enter a release date!")
            return
        if artist_name == "Select Artist" or artist_name is None:
            messagebox.showerror("Missing Field", "Please select an artist!")
            return
        if genre_name == "Select Genre" or genre_name is None:
            messagebox.showerror("Missing Field", "Please select a genre!")
            return
        if record_label_name == "Select Record Label" or record_label_name is None:
            messagebox.showerror("Missing Field", "Please select a record label!")
            return
        album = RecordAlbum.create_by_name(album_name=album_name, release_date=release_date, artist_name=artist_name,
                                           genre_name=genre_name, record_label_name=record_label_name)
        self.load_albums()
        child.grab_release()
        child.destroy()
        child.update()

    def update_album(self, child, album_name, release_date, artist_name, genre_name, record_label_name):
        if album_name == "" or album_name is None:
            messagebox.showerror("Missing Field", "Please enter an album name!")
            return
        if release_date == "" or release_date is None:
            messagebox.showerror("Missing Field", "Please enter a release date!")
            return
        if artist_name == "Select Artist" or artist_name is None:
            messagebox.showerror("Missing Field", "Please select an artist!")
            return
        if genre_name == "Select Genre" or genre_name is None:
            messagebox.showerror("Missing Field", "Please select a genre!")
            return
        if record_label_name == "Select Record Label" or record_label_name is None:
            messagebox.showerror("Missing Field", "Please select a record label!")
            return
        self.selected_album.album_name = album_name
        self.selected_album.release_date = release_date
        self.selected_album.artist_id = RecordArtist.read_by_name(artist_name).artist_id
        self.selected_album.genre_id = RecordGenre.read_by_name(genre_name).genre_id
        self.selected_album.record_label_id = RecordLabel.read_by_name(record_label_name).record_label_id
        self.selected_album.update()
        self.load_albums()
        child.grab_release()
        child.destroy()
        child.update()

    def delete_album(self):
        self.selected_album.delete()
        self.load_albums()

    def cancel_album(self, child):
        self.selected_album = None
        self.selected_track = None
        child.grab_release()
        child.destroy()
        child.update()

if __name__ == '__main__':
    RecordAlbumUI()
