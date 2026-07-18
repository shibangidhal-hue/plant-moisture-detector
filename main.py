import customtkinter as ctk
from database import initialize_db
from plant import HomeFrame
from graph import GraphFrame
from theme import set_dark, set_light, set_system

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class PlantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        initialize_db()
        self.geometry("1200x700")
        self.title("Plant Moisture Detector")
        self.create_login_screen()

    def create_login_screen(self):
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(self.login_frame, text="Plant Moisture Detector", font=("Arial", 32, "bold"))
        title.pack(pady=40)

        self.username_entry = ctk.CTkEntry(self.login_frame, width=300, height=40, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self.login_frame, width=300, height=40, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        self.login_result = ctk.CTkLabel(self.login_frame, text="", font=("Arial", 14))
        self.login_result.pack(pady=10)

        login_btn = ctk.CTkButton(self.login_frame, text="Login", width=200, height=45, command=self.check_login)
        login_btn.pack(pady=20)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "1234":
            self.login_frame.pack_forget()
            self.create_dashboard()
        else:
            self.login_result.configure(text="❌ Invalid Username or Password", text_color="#ff4a4a")

    def create_dashboard(self):
        self.sidebar = ctk.CTkFrame(self, width=220)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        side_title = ctk.CTkLabel(self.sidebar, text="Plant Manager", font=("Arial", 24, "bold"))
        side_title.pack(pady=25)

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.home_frame = HomeFrame(self.content_frame)
        self.graph_frame = GraphFrame(self.content_frame)

        self.home_frame.pack(fill="both", expand=True)

        home_btn = ctk.CTkButton(self.sidebar, text="🌱 Home Panel", command=self.show_home)
        home_btn.pack(pady=8, padx=15, fill="x")

        graph_btn = ctk.CTkButton(self.sidebar, text="📊 Graph Analytics", command=self.show_graph)
        graph_btn.pack(pady=8, padx=15, fill="x")

        sep = ctk.CTkLabel(self.sidebar, text="⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯", text_color="#444444")
        sep.pack(pady=15)

        dark_btn = ctk.CTkButton(self.sidebar, text="🌙 Dark Theme", fg_color="#333333", command=set_dark)
        dark_btn.pack(pady=5, padx=15, fill="x")

        light_btn = ctk.CTkButton(self.sidebar, text="☀️ Light Theme", fg_color="#777777", text_color="black", command=set_light)
        light_btn.pack(pady=5, padx=15, fill="x")

        system_btn = ctk.CTkButton(self.sidebar, text="💻 System Theme", fg_color="#555555", command=set_system)
        system_btn.pack(pady=5, padx=15, fill="x")

    def show_home(self):
        self.graph_frame.pack_forget()
        self.home_frame.pack(fill="both", expand=True)
        self.home_frame.load_history_from_db()

    def show_graph(self):
        self.home_frame.pack_forget()
        self.graph_frame.pack(fill="both", expand=True)
        self.graph_frame.refresh_dropdown_and_graph()


if __name__ == "__main__":
    app = PlantApp()
    app.mainloop()