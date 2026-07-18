import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import fetch_data, fetch_unique_plants, fetch_filtered_data


class GraphFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title = ctk.CTkLabel(self, text="Moisture Analytics Graph", font=("Arial", 28, "bold"))
        self.title.pack(pady=15)

        self.filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.filter_frame.pack(pady=5)

        self.filter_label = ctk.CTkLabel(self.filter_frame, text="Select Plant View:", font=("Arial", 14))
        self.filter_label.pack(side="left", padx=10)

        self.plant_dropdown = ctk.CTkOptionMenu(self.filter_frame, values=["All Plants"], command=self.on_filter_change)
        self.plant_dropdown.pack(side="left", padx=10)

        self.refresh_btn = ctk.CTkButton(self.filter_frame, text="🔄 Refresh Data", width=120, command=self.refresh_dropdown_and_graph)
        self.refresh_btn.pack(side="left", padx=10)

        self.chart_container = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_container.pack(fill="both", expand=True, padx=20, pady=10)

        self.canvas = None
        self.refresh_dropdown_and_graph()

    def refresh_dropdown_and_graph(self) -> None:
        current_selection = self.plant_dropdown.get()
        unique_plants = fetch_unique_plants()
        
        # Clean tuple structure extraction
        clean_plants = [p[0] if isinstance(p, tuple) else p for p in unique_plants]
        dropdown_options = ["All Plants"] + clean_plants
        
        self.plant_dropdown.configure(values=dropdown_options)
        if current_selection in dropdown_options:
            self.plant_dropdown.set(current_selection)
        else:
            self.plant_dropdown.set("All Plants")
            
        self.plot_analytics_chart()

    def on_filter_change(self, choice: str) -> None:
        self.plot_analytics_chart()

    def plot_analytics_chart(self) -> None:
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        selected_plant = self.plant_dropdown.get()
        records = fetch_data() if selected_plant == "All Plants" else fetch_filtered_data(selected_plant)
        
        if not records:
            for child in self.chart_container.winfo_children():
                child.destroy()
            self.no_data_lbl = ctk.CTkLabel(self.chart_container, text="❌ No moisture tracking data found.", font=("Arial", 16))
            self.no_data_lbl.pack(expand=True)
            return
            
        for child in self.chart_container.winfo_children():
            child.destroy()

        # Safe index parsing loops
        timestamps = [f"Log #{row[0]}" for row in records if len(row) >= 1]
        moisture_levels = [int(row[2]) for row in records if len(row) >= 3]
        plant_names = [row[1] if len(row) >= 2 else "Unknown" for row in records]

        fig, ax = plt.subplots(figsize=(7, 4), facecolor="#2b2b2b")
        ax.set_facecolor="#1e1e1e"

        ax.plot(timestamps, moisture_levels, color="#2fa572", marker="o", linewidth=2.5, markersize=6)

        for i, name in enumerate(plant_names):
            label_text = f" ({moisture_levels[i]}%)" if selected_plant != "All Plants" else f" {name} ({moisture_levels[i]}%)"
            ax.annotate(label_text, (timestamps[i], moisture_levels[i]), textcoords="offset points", xytext=(0,10), ha="center", color="white", fontsize=9, weight="bold")

        ax.set_title(f"Moisture Timeline: {selected_plant}", color="white", fontsize=14, pad=15, weight="bold")
        ax.set_ylim(-5, 105)
        ax.spines["bottom"].set_color("#444444")
        ax.spines["left"].set_color("#444444")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(colors="white", labelsize=9)
        ax.grid(True, linestyle="--", alpha=0.15, color="white")

        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)
