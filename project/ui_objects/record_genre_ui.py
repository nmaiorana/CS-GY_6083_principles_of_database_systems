# Create a window to manage record genres The window will create or modify RecordGenres objects. The window should
# have a dropdown to select or enter a new record genre name. Add a new button to create a new record with just the
# genre_name and genre_description

import tkinter as tk
from tkinter import messagebox
from project.business_objects.record_genres import RecordGenres


class RecordGenreUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Record Genre Manager')
        self.root.geometry('300x200')
        self.genre_name = tk.StringVar()
        self.genre_description = tk.StringVar()
        self.genre_list = tk.StringVar()
        self.genre_list.set('Select Genre')
        self.genres = RecordGenres.read_all()
        self.genre_names = [genre.genre_name for genre in self.genres]
        self.genre_id = None
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        tk.Label(self.root, text='Genre Name').grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.genre_name).grid(row=0, column=1)
        tk.Label(self.root, text='Genre Description').grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.genre_description).grid(row=1, column=1)
        tk.Button(self.root, text='Create Genre', command=self.create_genre).grid(row=2, column=0)
        tk.Button(self.root, text='Update Genre', command=self.update_genre).grid(row=2, column=1)
        tk.OptionMenu(self.root, self.genre_list, *self.genre_names, command=self.select_genre).grid(row=3, column=0)
        tk.Button(self.root, text='Delete Genre', command=self.delete_genre).grid(row=3, column=1)

    def reset_window(self):
        self.genres = RecordGenres.read_all()
        self.genre_names = [genre.genre_name for genre in self.genres]
        self.genre_list.set('Select Genre')
        print(f'Genres: {self.genre_names}')

    def select_genre(self, genre_name):
        print(f'Selected genre: {genre_name}')
        genre = RecordGenres.read_by_name(genre_name)
        self.genre_name.set(genre[0].genre_name)
        self.genre_description.set(genre[0].genre_description)
        self.genre_id = genre[0].genre_id
        self.reset_window()

    def create_genre(self):
        genre = RecordGenres.create(self.genre_name.get(), self.genre_description.get())
        messagebox.showinfo('Genre Created', f'Genre {genre.genre_name} created with id {genre.genre_id}')
        self.reset_window()

    def update_genre(self):
        genre = RecordGenres.read_by_name(self.genre_name.get())
        if genre:
            genre[0].genre_description = self.genre_description.get()
            updated_genre = RecordGenres.update(genre[0])
            messagebox.showinfo('Genre Updated',
                                f'Genre {updated_genre.genre_name} updated with id {updated_genre.genre_id}')
            self.reset_window()
        else:
            messagebox.showerror('Genre Not Found', f'Genre {self.genre_name.get()} not found')

    def delete_genre(self):
        if self.genre_id:
            RecordGenres.delete(self.genre_id)
            messagebox.showinfo('Genre Deleted', f'Genre {self.genre_name.get()} deleted with id {self.genre_id}')
            self.reset_window()
        else:
            messagebox.showerror('Genre Not Selected', f'Genre {self.genre_name.get()}')


if __name__ == '__main__':
    RecordGenreUI()
