# Create a window to manage record genres The window will create or modify RecordGenres objects. The window should
# have a dropdown to select or enter a new record genre name. Add a new button to create a new record with just the
# genre_name and genre_description

import tkinter as tk
from tkinter import messagebox, OptionMenu
from project.business_objects.record_genres_sql import RecordGenre


class RecordGenreUI:
    def __init__(self):
        self.optionMenu = None
        self.root = tk.Tk()
        self.root.title('Record Genre Manager')
        self.root.geometry('400x200')
        self.genre_name = tk.StringVar()
        self.genre_description = tk.StringVar()
        self.genre_selected = tk.StringVar()
        self.genre_selected.set('Select Genre')
        self.genres = RecordGenre.read_all()
        self.genre_names = [genre.genre_name for genre in self.genres]
        self.genre_id = None
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        self.optionMenu = OptionMenu(self.root, self.genre_selected, *self.genre_names, command=self.select_genre)
        self.optionMenu.grid(row=0, column=0)
        tk.Label(self.root, text='Genre Name').grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.genre_name).grid(row=1, column=1)
        tk.Label(self.root, text='Genre Description').grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.genre_description).grid(row=2, column=1)
        tk.Button(self.root, text='Create Genre', command=self.create_genre).grid(row=5, column=0)
        tk.Button(self.root, text='Update Genre', command=self.update_genre).grid(row=5, column=1)
        tk.Button(self.root, text='Delete Genre', command=self.delete_genre).grid(row=5, column=2)

    def reset_window(self):
        self.optionMenu.children['menu'].delete(0, 'end')
        self.genres = RecordGenre.read_all()
        [self.optionMenu.children["menu"].add_command(label=genre.genre_name,
                                                      command=lambda  x=genre.genre_name: self.select_genre(x))
         for genre in self.genres]
        self.genre_selected.set('Select Genre')
        print(f'Genres: {self.genre_names}')

    def select_genre(self, genre_name):
        print(f'Selected genre: {genre_name}')
        record = RecordGenre.read_by_name(genre_name)
        if not record:
            messagebox.showerror('Genre Not Found', f'Genre {genre_name} not found')
            return
        self.genre_name.set(record.genre_name)
        self.genre_description.set(record.genre_description)
        self.genre_id = record.genre_id

    def create_genre(self):
        record = RecordGenre.read_by_name(self.genre_name.get())
        if record:
            messagebox.showerror('Genre Exists', f'Genre {self.genre_name.get()} already exists')
            return
        record = RecordGenre.create(self.genre_name.get(), self.genre_description.get())
        self.genre_name.set(record.genre_name)
        self.genre_description.set(record.genre_description)
        self.genre_id = record.genre_id
        messagebox.showinfo('Genre Created', f'Genre {record.genre_name} created with id {record.genre_id}')
        self.reset_window()

    def update_genre(self):
        record = RecordGenre.read(self.genre_id)
        if record:
            record.genre_name = self.genre_name.get()
            record.genre_description = self.genre_description.get()
            record.update()
            messagebox.showinfo('Genre Updated',
                                f'Genre {record.genre_name} updated with id {record.genre_id}')
            self.reset_window()
        else:
            messagebox.showerror('Genre Not Found', f'Genre {self.genre_name.get()} not found')

    def delete_genre(self):
        if self.genre_id:
            record = RecordGenre.read(self.genre_id)
            record.delete()
            messagebox.showinfo('Genre Deleted', f'Genre {record.genre_name} deleted with id {record.genre_id}')
            self.genre_name.set('')
            self.genre_description.set('')
            self.genre_id = None
            self.reset_window()
        else:
            messagebox.showerror('Genre Not Selected', f'Genre {self.genre_name.get()}')


if __name__ == '__main__':
    RecordGenreUI()
