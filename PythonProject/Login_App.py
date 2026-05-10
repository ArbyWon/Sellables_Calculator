import customtkinter as ctk
import json
import os

DB_FILE = "arby_database.json"

class Database:
    @staticmethod
    def load():
        if not os.path.exists(DB_FILE): return {}
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return {}

    @staticmethod
    def save(data):
        with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller, colors):
        super().__init__(parent, fg_color=colors["panel_bg"], corner_radius=20)
        self.controller = controller
        self.colors = colors

        ctk.CTkLabel(self, text="Welcome to", font=("Helvetica", 16)).pack(pady=(50, 0))
        ctk.CTkLabel(self, text="Sellables\n conversion", font=("Helvetica", 32, "bold"), text_color=colors["accent"]).pack(pady=(0, 30))

        self.user_var, self.pass_var, self.msg_var = ctk.StringVar(), ctk.StringVar(), ctk.StringVar()

        # USERNAME SECTION
        ctk.CTkLabel(self, text="Username", font=("Helvetica", 13, "bold")).pack(anchor="w", padx=40)
        ctk.CTkEntry(self, textvariable=self.user_var, placeholder_text="Username", fg_color=colors["entry_bg"], border_width=0, height=45).pack(fill="x", padx=40, pady=(0, 15))

        # PASSWORD SECTION
        ctk.CTkLabel(self, text="Password", font=("Helvetica", 13, "bold")).pack(anchor="w", padx=40)
        ctk.CTkEntry(self, textvariable=self.pass_var, placeholder_text="Password", show="*", fg_color=colors["entry_bg"], border_width=0, height=45).pack(fill="x", padx=40, pady=(0, 10))

        ctk.CTkLabel(self, textvariable=self.msg_var, text_color=colors["accent"]).pack()

        ctk.CTkButton(self, text="Login", fg_color=colors["accent"], text_color=colors["btn_text"], height=45, command=self.login).pack(fill="x", padx=40, pady=5)
        ctk.CTkButton(self, text="Create Account", fg_color=colors["output_bg"], height=45, command=self.register).pack(fill="x", padx=40, pady=5)
        
        # EXIT APP BUTTON
        ctk.CTkButton(self, text="Exit App", font=("Helvetica", 14, "bold"), fg_color=colors.get("exit_red", "#C0392B"), hover_color=colors.get("exit_hover", "#A93226"), height=45, command=self.controller.destroy).pack(fill="x", padx=40, pady=(15, 5))

    def login(self):
        db = Database.load()
        u, p = self.user_var.get(), self.pass_var.get()
        if u in db and db[u]["password"] == p:
            self.controller.login_success(u)
        else: self.msg_var.set("❌ Invalid Credentials")

    def register(self):
        db = Database.load()
        u, p = self.user_var.get(), self.pass_var.get()
        if not u or not p: self.msg_var.set("❌ Fill all fields")
        elif u in db: self.msg_var.set("❌ User exists")
        else:
            db[u] = {"password": p, "inventory": {}}
            Database.save(db)
            self.msg_var.set("✅ Created!")

class InventoryPage(ctk.CTkFrame):
    def __init__(self, parent, controller, colors, page_data):
        super().__init__(parent, fg_color=colors["panel_bg"], corner_radius=20)
        self.controller, self.colors = controller, colors
        self.items = [i for cat in page_data.values() for i in cat["items"].keys()]

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header, text="My Vault", font=("Helvetica", 24, "bold"), text_color=colors["accent"]).pack(side="left")
        ctk.CTkButton(header, text="Back", width=60, command=lambda: self.controller.show_frame("MainMenu")).pack(side="right")

        add_f = ctk.CTkFrame(self, fg_color=colors["output_bg"], corner_radius=15)
        add_f.pack(fill="x", padx=15, pady=10, ipadx=10, ipady=10)
        
        self.item_var = ctk.StringVar(value=self.items[0])
        ctk.CTkOptionMenu(add_f, variable=self.item_var, values=self.items).pack(fill="x", padx=10, pady=5)
        
        self.qty_var = ctk.StringVar()
        ctk.CTkEntry(add_f, textvariable=self.qty_var, placeholder_text="Qty").pack(side="left", fill="x", expand=True, padx=10)
        ctk.CTkButton(add_f, text="Save", width=60, command=self.add).pack(side="right", padx=10)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=colors["entry_bg"], corner_radius=15)
        self.scroll.pack(fill="both", expand=True, padx=15, pady=15)

    def refresh_inventory(self):
        for w in self.scroll.winfo_children(): w.destroy()
        inv = Database.load().get(self.controller.current_user, {}).get("inventory", {})
        for item, qty in inv.items():
            f = ctk.CTkFrame(self.scroll, fg_color="transparent")
            f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"{item}: {qty:,}").pack(side="left")
            ctk.CTkButton(f, text="X", width=30, fg_color="#C0392B", command=lambda i=item: self.delete(i)).pack(side="right")

    def add(self):
        db = Database.load()
        user = self.controller.current_user
        item, qty = self.item_var.get(), int(self.qty_var.get() or 0)
        db[user]["inventory"][item] = db[user]["inventory"].get(item, 0) + qty
        Database.save(db)
        self.refresh_inventory()

    def delete(self, item):
        db = Database.load()
        del db[self.controller.current_user]["inventory"][item]
        Database.save(db)
        self.refresh_inventory()