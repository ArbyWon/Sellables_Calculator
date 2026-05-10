import os
import sys

# Check if the app is running as a compiled .exe
if not getattr(sys, 'frozen', False):
    # We are running locally as a .py script, use the hardcoded bypass
    os.environ['TCL_LIBRARY'] = r'C:\Program Files\Python313\tcl\tcl8.6'
    os.environ['TK_LIBRARY'] = r'C:\Program Files\Python313\tcl\tk8.6'

import customtkinter as ctk
from Login_App import LoginPage, InventoryPage, Database

# CONFIGURATION & STYLING
COLORS = {
    "app_bg": "#38748C", "panel_bg": "#51A5C1", "accent": "#64CFA1",        
    "accent_hover": "#4FB88C", "btn_text": "#1A4031", "text_light": "#FFFFFF",    
    "entry_bg": "#214A5E", "entry_fg": "#FFFFFF", "output_bg": "#2E6278",
    "exit_red": "#C0392B", "exit_hover": "#A93226"
}

PAGE_DATA = {
    "Shell": {"title": "Shells", "base_unit_name": "Trochus", "items": {"Aerolata": 3, "Scallop": 5, "Sand Dollar": 5, "Starfish": 7}},
    "Mushroom": {"title": "Mushrooms", "base_unit_name": "Trochus", "items": {"Plain Mushroom": 5, "Yellow Mushroom": 5, "Red Mushroom": 5, "Purple Mushroom": 5}},
    "Trash": {"title": "Trash", "base_unit_name": "Trochus", "items": {"Paper": 4, "Broken Bottle": 5, "Old Newspaper": 4, "Old Tire": 6}},
    "Body Part": {"title": "Body Parts", "base_unit_name": "Trochus", "items": {"Heart": 5, "Hand": 3, "Foot": 3, "Eyes": 4, "Brain": 5, "Bone": 3}},
    "Crab Shell": {"title": "Crab Shells", "base_unit_name": "Trochus", "items": {"Red Crab Shells": 6, "Black Crab Shells": 6, "Yellow Crab Shells": 6, "Blue Crab Shells": 6, "Green Crab Shells": 6}},
    "Mineral": {"title": "Minerals", "base_unit_name": "Trochus", "items": {"Sapphire": 7, "Ruby": 7, "Emerald": 8, "Diamond": 7, "Gold": 7, "Gypsum": 5, "Quartz": 5, "Copper": 5, "Silver": 5, "Lead": 5, "Iron": 5}}
}

ctk.set_appearance_mode("dark")

class ITANG_Sconversion(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sellables conversion")
        
        # Adjustable resolution based on screen size
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{int(screen_width * 0.2)}x{int(screen_height * 0.7)}") 
        
        self.configure(fg_color=COLORS["app_bg"])
        self.resizable(True, True)

        self.current_user = None

        self.container = ctk.CTkFrame(self, fg_color=COLORS["app_bg"], corner_radius=0)
        self.container.pack(fill="both", expand=True, padx=15, pady=15)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # Initialize Pages
        self.frames["LoginPage"] = LoginPage(self.container, self, COLORS)
        self.frames["LoginPage"].grid(row=0, column=0, sticky="nsew")

        self.frames["InventoryPage"] = InventoryPage(self.container, self, COLORS, PAGE_DATA)
        self.frames["InventoryPage"].grid(row=0, column=0, sticky="nsew")

        self.frames["HistoryPage"] = HistoryPage(self.container, self, COLORS)
        self.frames["HistoryPage"].grid(row=0, column=0, sticky="nsew")

        self.frames["MainMenu"] = MainMenuPage(self.container, self)
        self.frames["MainMenu"].grid(row=0, column=0, sticky="nsew")

        for page_id, data in PAGE_DATA.items():
            frame = CalculatorPageTemplate(self.container, self, page_id, data)
            self.frames[page_id] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.frames["RealMoney"] = CurrencyConverterPage(self.container, self)
        self.frames["RealMoney"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        self.frames[page_name].tkraise()

    def login_success(self, username):
        self.current_user = username
        self.frames["InventoryPage"].refresh_inventory() 
        self.frames["HistoryPage"].refresh_history()
        self.frames["MainMenu"].update_welcome_text(username)
        self.show_frame("MainMenu")
        
    def logout(self):
        self.current_user = None
        self.show_frame("LoginPage")

class MainMenuPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLORS["panel_bg"], corner_radius=20)
        self.controller = controller

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 0))
        self.welcome_lbl = ctk.CTkLabel(header, text="Welcome", font=("Helvetica", 14), text_color=COLORS["text_light"])
        self.welcome_lbl.pack(side="left")
        ctk.CTkButton(header, text="Logout", width=50, font=("Helvetica", 10, "bold"), fg_color=COLORS["output_bg"], command=self.controller.logout).pack(side="right")
        
        ctk.CTkLabel(self, text="Sellables\n conversion", font=("Helvetica", 32, "bold"), text_color=COLORS["accent"]).pack(pady=(10, 20))

        ctk.CTkButton(self, text="My Vault", font=("Helvetica", 15, "bold"), fg_color=COLORS["output_bg"], height=45, command=lambda: self.controller.show_frame("InventoryPage")).pack(fill="x", padx=40, pady=(0, 10))
        
        ctk.CTkButton(self, text="Sales History", font=("Helvetica", 15, "bold"), fg_color=COLORS["output_bg"], height=45, command=lambda: self.controller.show_frame("HistoryPage")).pack(fill="x", padx=40, pady=(0, 15))

        # Dynamically create category buttons
        for page_id in PAGE_DATA.keys():
            ctk.CTkButton(self, text=page_id, font=("Helvetica", 15, "bold"), fg_color=COLORS["accent"], text_color=COLORS["btn_text"], height=40, command=lambda i=page_id: self.controller.show_frame(i)).pack(fill="x", padx=40, pady=6)

        ctk.CTkButton(self, text="Real Money ($)", font=("Helvetica", 15, "bold"), fg_color=COLORS["output_bg"], height=45, command=lambda: self.controller.show_frame("RealMoney")).pack(fill="x", padx=40, pady=15)

        #EXIT BUTTON
        ctk.CTkButton(self, text="Exit App", font=("Helvetica", 14, "bold"), fg_color=COLORS["exit_red"], hover_color=COLORS["exit_hover"], height=40, command=self.controller.destroy).pack(fill="x", padx=40, pady=(20, 0))

    def update_welcome_text(self, username):
        self.welcome_lbl.configure(text=f"Welcome, {username}!")

class HistoryPage(ctk.CTkFrame):
    def __init__(self, parent, controller, colors):
        super().__init__(parent, fg_color=colors["panel_bg"], corner_radius=20)
        self.controller = controller
        self.colors = colors

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header, text="Top Selling Items", font=("Helvetica", 24, "bold"), text_color=colors["accent"]).pack(side="left")
        ctk.CTkButton(header, text="Back", width=60, command=lambda: self.controller.show_frame("MainMenu")).pack(side="right")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=colors["entry_bg"], corner_radius=15)
        self.scroll.pack(fill="both", expand=True, padx=15, pady=15)

    def refresh_history(self):
        for w in self.scroll.winfo_children(): w.destroy()
        
        if not self.controller.current_user: return
        
        db = Database.load()
        user_data = db.get(self.controller.current_user, {})
        history = user_data.get("history", {})
        
        if not history:
            ctk.CTkLabel(self.scroll, text="No sales recorded yet. Sell items in Categories!", text_color=self.colors["text_light"]).pack(pady=20)
            return

        sorted_history = sorted(history.items(), key=lambda x: x[1], reverse=True)
        
        for index, (item, qty) in enumerate(sorted_history, start=1):
            f = ctk.CTkFrame(self.scroll, fg_color="transparent")
            f.pack(fill="x", pady=5)
            ctk.CTkLabel(f, text=f"#{index}", font=("Helvetica", 14, "bold"), text_color=self.colors["text_light"]).pack(side="left", padx=(10, 5))
            ctk.CTkLabel(f, text=f"{item}", font=("Helvetica", 14, "bold"), text_color=self.colors["accent"]).pack(side="left")
            ctk.CTkLabel(f, text=f"Total Sold: {qty:,}", font=("Helvetica", 14)).pack(side="right", padx=10)

class CurrencyConverterPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLORS["panel_bg"], corner_radius=20)
        self.controller = controller
        self.inputs = {}
        self.output_vars = {}

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(25, 10))
        ctk.CTkLabel(header, text="Cash Out", font=("Helvetica", 24, "bold"), text_color=COLORS["accent"]).pack(side="left")
        ctk.CTkButton(header, text="Back", width=60, command=lambda: self.controller.show_frame("MainMenu")).pack(side="right")

        inputs_frame = ctk.CTkFrame(self, fg_color="transparent")
        inputs_frame.pack(fill="both", expand=True, padx=20, pady=10)

        for label in ["Total Trochus", "Trochus per 50 PHP", "Trochus per 1 USD"]:
            ctk.CTkLabel(inputs_frame, text=label, font=("Helvetica", 12, "bold"), text_color=COLORS["text_light"]).pack(anchor="w", pady=(8, 2))
            var = ctk.StringVar()
            var.trace_add("write", self.calculate)
            self.inputs[label] = var
            ctk.CTkEntry(inputs_frame, textvariable=var, fg_color=COLORS["entry_bg"], border_width=0, height=35).pack(fill="x")

        output_container = ctk.CTkFrame(self, fg_color=COLORS["output_bg"], corner_radius=15)
        output_container.pack(side="bottom", fill="x", padx=15, pady=20, ipadx=10, ipady=10)

        for field in ["Total PHP", "Total USD"]:
            ctk.CTkLabel(output_container, text=field, font=("Helvetica", 12, "bold"), text_color=COLORS["accent"]).pack(anchor="w", padx=10)
            var = ctk.StringVar(value="₱ 0.00")
            self.output_vars[field] = var
            ctk.CTkLabel(output_container, textvariable=var, font=("Helvetica", 18, "bold")).pack(anchor="w", padx=10, pady=(0, 10))

    def calculate(self, *args):
        try:
            t = float(self.inputs["Total Trochus"].get() or 0)
            p_r = float(self.inputs["Trochus per 50 PHP"].get() or 0)
            u_r = float(self.inputs["Trochus per 1 USD"].get() or 0)
            self.output_vars["Total PHP"].set(f"₱ {(t/p_r)*50:,.2f}" if p_r > 0 else "₱ 0.00")
            self.output_vars["Total USD"].set(f"$ {t/u_r:,.2f}" if u_r > 0 else "$ 0.00")
        except: pass

class CalculatorPageTemplate(ctk.CTkFrame):
    def __init__(self, parent, controller, page_id, data):
        super().__init__(parent, fg_color=COLORS["panel_bg"], corner_radius=20)
        self.controller = controller
        self.items_dict = data["items"]
        self.base_unit = data["base_unit_name"]
        self.inputs = {}

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(25, 5))
        ctk.CTkLabel(header, text=data["title"], font=("Helvetica", 24, "bold"), text_color=COLORS["accent"]).pack(side="left")
        ctk.CTkButton(header, text="Back", width=60, command=lambda: self.controller.show_frame("MainMenu")).pack(side="right")

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20)

        for item, price in self.items_dict.items():
            ctk.CTkLabel(scroll, text=f"{item} ({price} G)", font=("Helvetica", 11, "bold")).pack(anchor="w")
            var = ctk.StringVar()
            var.trace_add("write", self.calculate)
            self.inputs[item] = var
            ctk.CTkEntry(scroll, textvariable=var, fg_color=COLORS["entry_bg"], border_width=0, height=30).pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(scroll, text="Ratio ($)", font=("Helvetica", 11, "bold")).pack(anchor="w")
        self.ratio_var = ctk.StringVar()
        self.ratio_var.trace_add("write", self.calculate)
        ctk.CTkEntry(scroll, textvariable=self.ratio_var, fg_color=COLORS["entry_bg"], border_width=0, height=30).pack(fill="x")

        out = ctk.CTkFrame(self, fg_color=COLORS["output_bg"], corner_radius=15)
        out.pack(side="bottom", fill="x", padx=15, pady=20, ipadx=10, ipady=5)
        
        self.total_g = ctk.StringVar(value="0")
        self.total_b = ctk.StringVar(value="0")
        ctk.CTkLabel(out, text="Total Gralats", text_color=COLORS["accent"]).pack(anchor="w", padx=10)
        ctk.CTkLabel(out, textvariable=self.total_g, font=("Helvetica", 16, "bold")).pack(anchor="w", padx=10)
        ctk.CTkLabel(out, text=self.base_unit, text_color=COLORS["accent"]).pack(anchor="w", padx=10)
        ctk.CTkLabel(out, textvariable=self.total_b, font=("Helvetica", 16, "bold")).pack(anchor="w", padx=10)

        # Autofill Controls Frame
        autofill_frame = ctk.CTkFrame(out, fg_color="transparent")
        autofill_frame.pack(fill="x", padx=10, pady=(10, 0))

        # Dynamically get unique G values for the dropdown
        unique_prices = sorted(list(set(self.items_dict.values())))
        autofill_options = ["All"] + [f"{p}G Only" for p in unique_prices]
        
        self.filter_var = ctk.StringVar(value="All")
        ctk.CTkOptionMenu(autofill_frame, variable=self.filter_var, values=autofill_options, width=110, fg_color=COLORS["entry_bg"]).pack(side="left", padx=(0, 5))
        ctk.CTkButton(autofill_frame, text="Auto-fill", font=("Helvetica", 12, "bold"), fg_color=COLORS["entry_bg"], height=30, command=self.fill_from_inventory).pack(side="left", fill="x", expand=True)
        
        # Record Sale Button
        ctk.CTkButton(out, text="Record Sale", font=("Helvetica", 12, "bold"), fg_color=COLORS["accent"], text_color=COLORS["btn_text"], height=35, command=self.record_sale).pack(fill="x", padx=10, pady=(10, 0))

    def calculate(self, *args):
        g = sum(int(v.get() or 0) * self.items_dict[k] for k, v in self.inputs.items() if v.get().isdigit())
        r = float(self.ratio_var.get() or 1)
        self.total_g.set(f"{g:,}")
        self.total_b.set(f"{g/r:,.2f}" if r > 0 else "0")

    def fill_from_inventory(self):
        try:
            db = Database.load()
            user = self.controller.current_user
            if not user: return
            inv = db.get(user, {}).get("inventory", {})
            
            selected_filter = self.filter_var.get()
            
            for item_name, var in self.inputs.items():
                var.set("") # Clear fields first to ensure a clean autofill
                item_price = self.items_dict[item_name]
                
                # Check if the item matches the selected filter
                if selected_filter == "All" or selected_filter == f"{item_price}G Only":
                    if item_name in inv and inv[item_name] > 0:
                        var.set(str(inv[item_name]))
        except: pass

    def record_sale(self):
        try:
            db = Database.load()
            user = self.controller.current_user
            if not user: return
            if "history" not in db[user]: db[user]["history"] = {}
            if "inventory" not in db[user]: db[user]["inventory"] = {}
            
            recorded = False
            for k, v in self.inputs.items():
                if v.get().isdigit() and int(v.get()) > 0:
                    qty = int(v.get())
                    # Add to History
                    db[user]["history"][k] = db[user]["history"].get(k, 0) + qty
                    # Deduct from Inventory Vault
                    if k in db[user]["inventory"]:
                        db[user]["inventory"][k] = max(0, db[user]["inventory"][k] - qty)
                        if db[user]["inventory"][k] == 0:
                            del db[user]["inventory"][k]
                    v.set("") 
                    recorded = True
            
            if recorded:
                Database.save(db)
                self.controller.frames["HistoryPage"].refresh_history()
                self.controller.frames["InventoryPage"].refresh_inventory()
        except: pass

if __name__ == "__main__":
    app = ITANG_Sconversion()
    app.mainloop()