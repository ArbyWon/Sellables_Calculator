# Sellables Conversion Application
**Software Design Project**

## Overview
The Sellables Conversion Application is a lightweight, standalone Windows desktop tool built with Python and CustomTkinter. It is designed to help users calculate the conversion values for various in-game items (such as Shells, Mushrooms, Trash, Body Parts, etc.) into a base unit (Trochus) and total Gralats. It also features a built-in user authentication system and personal inventory management.

## System Features
1. **Secure Authentication:** Local login and registration system that ensures users only see and edit their own data.
2. **Dynamic Item Calculators:** Calculate Total Gralats based on item quantities and a user-defined Ratio ($). Covers multiple categories including Shells, Mushrooms, Trash, Body Parts, Crab Shells, and Minerals.
3. **Inventory Management:** Add, view, and delete specific items. Inventory changes are securely tied to the current user's active session.
4. **Real Money Conversion:** A dedicated module to convert in-game assets into real-world currency equivalents.
5. **Serverless Local Storage:** Operates completely offline using a local JSON database (`arby_database.json`).

## Tech Stack
* **Frontend:** CustomTkinter (Modern GUI toolkit for Python)
* **Backend:** Python 3.13.3
* **Database:** JSON (Built-in Python `json` library for local data persistence)

## Prerequisites
* **Python 3.13 and up** installed on your system.
* **CustomTkinter library:** Required for the modern user interface.
  * Install via terminal: `pip install customtkinter`
 
  ## How to run EXE file
If you prefer not to install Python or run the source code, you can use the pre-compiled executable:
1. Locate the `main.exe` file in dist folder.
2. Double-click the `main.exe` file to launch the application immediately.

## How to Run the source code
1. Navigate to the project root directory in your terminal or command prompt.
2. Ensure you have installed the required `customtkinter` dependency.
3. Run the application using the following command:
   ```bash
   python main.py
