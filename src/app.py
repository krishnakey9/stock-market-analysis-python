import os
import tkinter as tk
from tkinter import ttk, messagebox

from data_loader import load_stock_data
from indicators import add_indicators
from visualizer import plot_dashboard

DATA_FOLDER = "data"


def get_available_stocks():
    return [f for f in os.listdir(DATA_FOLDER) if f.endswith(".json")]


def analyze_stock():
    stock_file = stock_var.get()

    if not stock_file:
        messagebox.showerror("Error", "Please select a stock file")
        return

    try:
        df = load_stock_data(os.path.join(DATA_FOLDER, stock_file))
        df = add_indicators(df)
        plot_dashboard(df)
    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- UI ----------------
root = tk.Tk()
root.title("Stock Market Analysis System")
root.geometry("420x240")

tk.Label(root, text="Select Stock", font=("Arial", 11)).pack(pady=(20, 5))

stock_var = tk.StringVar()
stock_dropdown = ttk.Combobox(
    root,
    textvariable=stock_var,
    values=get_available_stocks(),
    state="readonly",
    width=32
)
stock_dropdown.pack()

tk.Button(
    root,
    text="Load & Analyze",
    command=analyze_stock,
    bg="#2e86de",
    fg="white",
    width=22
).pack(pady=30)

root.mainloop()
