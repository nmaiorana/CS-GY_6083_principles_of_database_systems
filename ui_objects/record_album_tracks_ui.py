from tkinter import *
from tkinter import ttk
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


class RecordTracksUI:
    def __init__(self, window, album):
        self.track_view = None
        self.tracks = []
        self.selected_album = album
        self.selected_track = None
        if window is not None:
            self.primary = window
        else:
            self.primary = Tk()

        self.build_track_window(self.primary)
        self.load_tracks()

    def remove_tracks(self):
        for item in self.track_view.get_children():
            self.track_view.delete(item)

    def load_tracks(self):
        self.remove_tracks()
        self.selected_track = None
        self.tracks = self.selected_album.get_tracks()
        index = 0
        for track in self.tracks:
            self.track_view.insert("", "end", values=(track.track_name, track.track_number, track.genre_name()),
                                   iid=index)
            index += 1

    def build_track_window(self, album_entry):
        if album_entry is None:
            child = self.primary
        else:
            child = Toplevel(album_entry)
        child.grab_set()
        child.geometry("600x500")
        child.title(f"Tracks: {self.selected_album.album_name}")
        new_track_button = Button(child, text="New Track", padx=2, pady=3, command=lambda: self.create_new_track())
        new_track_button.grid(row=0, column=0, sticky="w")
        edit_track_button = Button(child, text="Edit Track", command=lambda: self.edit_selected_track())
        edit_track_button.grid(row=1, column=0, sticky="w")
        delete_track_button = Button(child, text="Delete Track", command=lambda: self.delete_selected_track())
        delete_track_button.grid(row=2, column=0, sticky="w")
        cancel_track_button = Button(child, text="Cancel", command=lambda: self.cancel_track_window(child))
        cancel_track_button.grid(row=3, column=0, sticky="w")

        self.track_view = ttk.Treeview(child, columns=("track_name", "track_number", "genre_name"),
                                       show="headings",
                                       height="20")

        self.track_view.grid(row=0, column=1, rowspan=10, columnspan=3)
        self.track_view.heading("track_name", text="Track Name", anchor="w")
        self.track_view.heading("track_number", text="Track Number", anchor="center")
        self.track_view.heading("genre_name", text="Genre", anchor="center")

        self.track_view.column("track_name", width=200)
        self.track_view.column("track_number", width=40)
        self.track_view.column("genre_name", width=200)

        self.load_tracks()

    def create_new_track(self):
        self.selected_track = None
        self.edit_track()

    def cancel_track_window(self, child):
        child.grab_release()
        child.destroy()
        child.update()

    def delete_selected_track(self):
        if self.track_view.selection() is None or len(self.track_view.selection()) == 0:
            messagebox.showerror("No Selection", "Please select a track to delete!")
            return
        selected_item = int(self.track_view.selection()[0])
        self.selected_track = self.tracks[selected_item]
        self.selected_track.delete()
        self.load_tracks()
        self.selected_track = None

    def edit_selected_track(self):
        if self.track_view.selection() is None or len(self.track_view.selection()) == 0:
            messagebox.showerror("No Selection", "Please select a track to edit!")
            return
        selected_item = int(self.track_view.selection()[0])
        self.selected_track = self.tracks[selected_item]
        self.edit_track()

    def edit_track(self):
        track_name = StringVar()
        track_number_selected = IntVar()
        track_number_range = range(1, 21)
        used_track_numbers = [track.track_number for track in self.selected_album.get_tracks()]
        track_number_range = [track_number for track_number in track_number_range if
                              track_number not in used_track_numbers]
        track_number_selected.set(track_number_range[0])
        genre_selected = StringVar()
        if self.selected_track is None:
            frame_title = "New Track"
            track_name.set("")
            genre_selected.set("Select Genre")
        else:
            frame_title = "Edit Track"
            track_name.set(self.selected_track.track_name)
            track_number_range.append(self.selected_track.track_number)
            track_number_selected.set(self.selected_track.track_number)
            genre_selected.set(self.selected_track.genre_name())

        track_number_range = sorted(track_number_range)
        track_child = Toplevel(self.track_view)
        track_child.title("Edit Tracks")
        track_child.geometry("600x450")
        track_child.grab_set()

        label_width = 20
        input_width = 60
        button_width = 10

        input_frame = LabelFrame(track_child, text="Enter/Edit track information", padx=5, pady=5)
        input_frame.grid(row=0, rowspan=6, column=0)

        track_name_label = Label(input_frame, text="Track Name", width=20, height=2, anchor="w", relief="ridge")
        track_number_label = Label(input_frame, text="Track Number", width=20, height=2, anchor="w", relief="ridge")
        genre_label = Label(input_frame, text="Genre", width=label_width, height=2, anchor="w", relief="ridge")

        track_name_label.grid(row=0, column=0, padx=1, pady=0)
        track_number_label.grid(row=1, column=0, padx=1, pady=0)
        genre_label.grid(row=2, column=0, padx=1, pady=0)

        track_name_entry = Entry(input_frame, textvariable=track_name, width=input_width)
        track_number_option_menu = OptionMenu(input_frame,
                                              track_number_selected,
                                              *track_number_range)
        track_number_option_menu.config(width=input_width)
        genre_option_menu = OptionMenu(input_frame,
                                       genre_selected,
                                       *[genre.genre_name for genre in RecordGenre.read_all()])
        genre_option_menu.config(width=input_width)

        track_name_entry.grid(row=0, column=1, padx=1, pady=0)
        track_number_option_menu.grid(row=1, column=1, padx=1, pady=0)
        genre_option_menu.grid(row=2, column=1, padx=1, pady=0)

        if self.selected_track is not None:
            update_track_button = Button(input_frame, text="Update",
                                         command=lambda: self.update_track(track_child,
                                                                           track_name.get(),
                                                                           track_number_selected.get(),
                                                                           genre_selected.get()))
            update_track_button.config(width=button_width)
            update_track_button.grid(row=4, column=0, padx=0, pady=1)
        else:
            add_track_button = Button(input_frame, text="Add",
                                      command=lambda: self.add_track(track_child,
                                                                     track_name.get(),
                                                                     track_number_selected.get(),
                                                                     genre_selected.get()))
            add_track_button.config(width=button_width)
            add_track_button.grid(row=4, column=0, padx=0, pady=1)

        cancel_button = Button(input_frame, text="Cancel", command=lambda: self.cancel_track(track_child))
        cancel_button.config(width=button_width)
        cancel_button.grid(row=4, column=2, padx=0, pady=1)

    def update_track(self, child, track_name, track_number, genre_name):
        self.selected_track.track_name = track_name
        self.selected_track.track_number = track_number
        self.selected_track.genre_id = RecordGenre.read_by_name(genre_name).genre_id
        self.selected_track.update()
        self.load_tracks()
        child.grab_release()
        child.destroy()
        child.update()
        self.update_album_summary()

    def add_track(self, child, track_name, track_number, genre_name):
        if track_name == "" or track_name is None:
            messagebox.showerror("Missing Field", "Please enter a track name!")
            return
        if track_number == "" or track_number is None:
            messagebox.showerror("Missing Field", "Please enter a track number!")
            return
        if genre_name == "Select Genre" or genre_name is None:
            messagebox.showerror("Missing Field", "Please select a genre!")
            return
        self.selected_album.add_track(track_name=track_name, track_number=track_number, genre_name=genre_name)
        self.load_tracks()
        child.grab_release()
        child.destroy()
        child.update()

    def cancel_track(self, child):
        self.selected_track = None
        child.grab_release()
        child.destroy()
        child.update()


if __name__ == '__main__':
    album = RecordAlbum.read_by_name("The Dark Side of the Moon")
    RecordTracksUI(None, album).primary.mainloop()
