import customtkinter as ctk
from database import save_data, fetch_data, clear_all_records


class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.load_history_from_db()

    def create_widgets(self):
        title = ctk.CTkLabel(self, text="Plant Moisture Checker", font=("Arial", 30, "bold"))
        title.pack(pady=20)

        plant_label = ctk.CTkLabel(self, text="Plant Name", font=("Arial", 16))
        plant_label.pack(pady=2)
        
        self.plant_entry = ctk.CTkEntry(self, width=350, height=40, placeholder_text="e.g., Monstera, Fern")
        self.plant_entry.pack(pady=5)

        moisture_label = ctk.CTkLabel(self, text="Moisture Value (%)", font=("Arial", 16))
        moisture_label.pack(pady=2)
        
        self.moisture_entry = ctk.CTkEntry(self, width=350, height=40, placeholder_text="Enter value (0 - 100)")
        self.moisture_entry.pack(pady=5)

        self.result_label = ctk.CTkLabel(self, text="", font=("Arial", 22, "bold"))
        self.result_label.pack(pady=15)

        check_btn = ctk.CTkButton(self, text="Check & Save Moisture", width=220, height=45, command=self.check_moisture)
        check_btn.pack(pady=10)

        history_title = ctk.CTkLabel(self, text="Saved Plant History", font=("Arial", 18, "bold"))
        history_title.pack(pady=(20, 5))

        self.history_box = ctk.CTkTextbox(self, width=600, height=200)
        self.history_box.pack(pady=5)

        # Clear History Action Button
        clear_btn = ctk.CTkButton(
            self, 
            text="🗑️ Clear All History", 
            fg_color="#A83232",       
            hover_color="#822020",
            width=180, 
            height=35, 
            command=self.clear_history
        )
        clear_btn.pack(pady=10)

    def check_moisture(self):
        plant = self.plant_entry.get().strip()
        moisture_raw = self.moisture_entry.get().strip()

        if not plant or not moisture_raw:
            self.result_label.configure(text="⚠️ Please fill in all fields", text_color="orange")
            return

        try:
            moisture = int(moisture_raw)
            if not (0 <= moisture <= 100):
                raise ValueError()
        except ValueError:
            self.result_label.configure(text="❌ Moisture must be a number between 0 and 100", text_color="red")
            return

        if moisture < 30:
            status, color = "Dry ⚠️", "#ff4a4a"
        elif moisture < 70:
            status, color = "Healthy ✅", "#2fa572"
        else:
            status, color = "Wet 💧", "#3b8ed0"

        self.result_label.configure(text=f"{plant} Status: {status}", text_color=color)
        save_data(plant, moisture, status)
        self.append_to_history_view(plant, moisture, status)

        self.plant_entry.delete(0, "end")
        self.moisture_entry.delete(0, "end")

    def append_to_history_view(self, name: str, moisture: int, status: str):
        self.history_box.configure(state="normal")
        self.history_box.insert("end", f"🌱 {name} | Moisture: {moisture}% | Status: {status}\n")
        self.history_box.configure(state="disabled")
        self.history_box.see("end")

    def load_history_from_db(self):
        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", "end")
        
        records = fetch_data()
        for row in records:
            if len(row) >= 4:
                name = row[1]
                moisture = row[2]
                status = row[3]
                self.history_box.insert("end", f"🌱 {name} | Moisture: {moisture}% | Status: {status}\n")
            
        self.history_box.configure(state="disabled")
        self.history_box.see("end")

    def clear_history(self):
        """Wipes the database table records clean and resets the history text view."""
        clear_all_records()
        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", "end")
        self.history_box.configure(state="disabled")
        self.result_label.configure(text="🗑️ History Cleared Successfully!", text_color="orange")
