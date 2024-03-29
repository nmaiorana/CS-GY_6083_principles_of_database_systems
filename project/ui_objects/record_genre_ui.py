# Create a window to manage record genres The window will create or modify RecordGenres objects. The window should
# have a dropdown to select or enter a new record genre name. Add a new button to create a new record with just the
# genre_name and genre_description

# import tkinter as tk
from tkinter import Tk
from tkinter import messagebox
from tkinter import OptionMenu
from tkinter import Button
from tkinter import Entry
from tkinter import Label
from tkinter import StringVar
# from customtkinter import CTk as Tk
# from customtkinter import CTkOptionMenu as OptionMenu
# from customtkinter import CTkButton as Button
# from customtkinter import CTkEntry as Entry
# from customtkinter import CTkLabel as Label
# from customtkinter import StringVar

from project.business_objects.record_genres_sql import RecordGenre


class RecordGenreUI:
    def __init__(self):
        self.optionMenu = None
        self.root = Tk()
        self.root.title('Record Genre Manager')
        self.root.geometry('500x200')
        self.genre_name = StringVar()
        self.genre_description = StringVar()
        self.genre_selected = StringVar()
        self.genre_selected.set('Select Genre')
        self.genres = RecordGenre.read_all()
        self.genre_names = [genre.genre_name for genre in self.genres]
        self.genre_id = None
        self.create_widgets()
        self.root.mainloop()
    def create_widgets(self):
        self.optionMenu = OptionMenu(self.root, self.genre_selected, *self.genre_names, command=lambda option: self.select_genre(option))
        self.optionMenu.grid(row=0, column=0)
        Label(self.root, text='Genre Name').grid(row=1, column=0)
        Entry(self.root, textvariable=self.genre_name).grid(row=1, column=1)
        Label(self.root, text='Genre Description').grid(row=2, column=0)
        Entry(self.root, textvariable=self.genre_description, width=40).grid(row=2, column=1)
        Button(self.root, text='Create Genre', command=self.create_genre).grid(row=5, column=0)
        Button(self.root, text='Update Genre', command=self.update_genre).grid(row=5, column=1)
        Button(self.root, text='Delete Genre', command=self.delete_genre).grid(row=5, column=2)

    def reset_window(self):
        self.optionMenu.children['menu'].delete(0, 'end')
        self.genres = RecordGenre.read_all()
        [self.optionMenu.children["menu"].add_command(label=genre.genre_name,
                                                      command=lambda  x=genre.genre_name: self.select_genre(x))
         for genre in self.genres]
        self.genre_selected.set('Select Genre')

    def select_genre(self, genre_name):
        record = RecordGenre.read_by_name(genre_name)
        if not record:
            self.display_error_message('Genre Not Found', f'Genre {genre_name}')
            return
        self.genre_name.set(record.genre_name)
        self.genre_description.set(record.genre_description)
        self.genre_id = record.genre_id

    def create_genre(self):
        if len(self.genre_name.get()) == 0:
            self.display_error_message('Genre Name Required', 'Genre Name Required')
            return
        record = RecordGenre.read_by_name(self.genre_name.get())
        if record:
            self.display_error_message('Genre Exists', f'Genre {self.genre_name.get()} already exists')
            return
        record = RecordGenre.create(self.genre_name.get(), self.genre_description.get())
        self.genre_name.set(record.genre_name)
        self.genre_description.set(record.genre_description)
        self.genre_id = record.genre_id
        self.display_info_message('Genre Created', f'Genre {record.genre_name} created with id {record.genre_id}')
        self.reset_window()

    def update_genre(self):
        if not self.genre_id:
            if len(self.genre_name.get()) != 0:
                self.display_error_message('Genre Not Created', 'Genre Not Created Yet')
                return
            self.display_error_message('Genre Not Selected', f'Genre Not Selected')
            return
        record = RecordGenre.read(self.genre_id)
        if not record:
            self.display_error_message('Genre Not Found', f'Genre {self.genre_name.get()}')

        record.genre_name = self.genre_name.get()
        record.genre_description = self.genre_description.get()
        record.update()
        self.display_info_message('Genre Updated', f'Genre {record.genre_name} updated with id {record.genre_id}')
        self.reset_window()


    def delete_genre(self):
        if not self.genre_id:
            if len(self.genre_name.get()) != 0:
                self.display_error_message('Genre Not Created', 'Genre Not Created Yet')
                return
            self.display_error_message('Genre Not Selected', f'Genre Not Selected')
            return

        record = RecordGenre.read(self.genre_id)
        record.delete()
        self.display_info_message('Genre Deleted', f'Genre {record.genre_name} deleted with id {record.genre_id}')
        self.genre_name.set('')
        self.genre_description.set('')
        self.genre_id = None
        self.reset_window()

    def display_info_message(self, title, message):
        messagebox.showinfo(title, message)

    def display_error_message(self, title, message):
        messagebox.showerror(title, message)



if __name__ == '__main__':
    RecordGenreUI()
