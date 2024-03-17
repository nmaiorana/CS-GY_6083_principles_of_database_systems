# This python script will create a class to view the band members.

from project.tools import db_utils as dbu
# Create a UI class to interact using customTkinter
import customtkinter


class BandMembers:
    def __init__(self, band_name):
        self.band_name = band_name

    def get_band_members(self):
        query = f"SELECT * FROM band_members WHERE artist_name = '{self.band_name}'"
        band_members = dbu.db_query_to_df(query)
        return band_members

    def add_band_member(self, member_id, artist_id, from_date, to_date):
        conn = dbu.connect_to_db()
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO band_members (member_id, artist_id, from_date, to_date) "
            f"VALUES ('{member_id}', '{artist_id}', '{from_date}', '{to_date}')")
        conn.commit()
        conn.close()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x180")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_2 = customtkinter.CTkCheckBox(self, text="checkbox 2")
        self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def button_callback(self):
        print("button pressed")


# Create an instance of the band members UI
class BandMembersUI(customtkinter.CTk):
    def __init__(self, band_name):
        super().__init__()

        self.title("Band Members")
        self.geometry("400x180")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.band_members = BandMembers(band_name)
        self.band_members_df = self.band_members.get_band_members()

        self.band_members_listbox = customtkinter.CTkCheckBox(self, self.band_members_df.index)
        self.band_members_listbox.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.band_members_listbox.bind("<<ListboxSelect>>", self.listbox_callback)

        self.add_band_member_button = customtkinter.CTkButton(self, text="Add Band Member", command=self.add_band_member)
        self.add_band_member_button.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="ew")

    def listbox_callback(self, event):
        selection = event.widget.curselection()
        value = event.widget.get(selection[0])
        print(f"selection: {value}")

    def add_band_member(self):
        print("add band member pressed")


app = BandMembersUI("Boston")
app.mainloop()
