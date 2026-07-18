import customtkinter as ctk

def set_dark() -> None:
    """Switch the global application theme to Dark Mode."""
    ctk.set_appearance_mode("dark")

def set_light() -> None:
    """Switch the global application theme to Light Mode."""
    ctk.set_appearance_mode("light")

def set_system() -> None:
    """Switch the theme to match the user's Operating System settings."""
    ctk.set_appearance_mode("system")
