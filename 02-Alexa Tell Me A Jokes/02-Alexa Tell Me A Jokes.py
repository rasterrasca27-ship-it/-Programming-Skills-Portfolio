import os
import random
import tkinter as tk
from tkinter import ttk, messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_JOKES = [
    "Why did the chicken cross the road?To get to the other side.",
    "What happens if you boil a clown?You get a laughing stock.",
    "Why don't scientists trust atoms?Because they make up everything.",
]

    
def get_jokes_file():
    """Find randomJokes.txt beside the script or in AlexaJokes, or create a default."""
    nested_path = os.path.join(BASE_DIR, "AlexaJokes", "randomJokes.txt")
    if os.path.isfile(nested_path):
        return nested_path

    for filename in ("randomJokes.txt", "randomjokes.txt"):
        path = os.path.join(BASE_DIR, filename)
        if os.path.isfile(path):
            return path

    default_path = os.path.join(BASE_DIR, "randomJokes.txt")
    with open(default_path, "w", encoding="utf-8") as file:
        file.write("\n".join(DEFAULT_JOKES) + "\n")
    return default_path


DATA_FILE = get_jokes_file()


def load_jokes(file_path):
    """Read the text file and return a list of (setup, punchline) tuples."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    jokes = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if "?" in line:
                setup, punchline = line.split("?", 1)
                setup = setup.strip() + "?"
            else:
                # Fallback if a line has no question mark
                setup, punchline = line, ""

            jokes.append((setup, punchline.strip()))

    return jokes


class JokeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Alexa - Joke Assistant")
        self.geometry("720x500")
        self.minsize(620, 420)
        self.resizable(True, True)
        self.configure(bg="#0b1020")

        self.setup_styles()

        try:
            self.jokes = load_jokes(DATA_FILE)
        except FileNotFoundError:
            messagebox.showerror(
                "File Not Found",
                f"Could not find {DATA_FILE}.\nPlease place randomJokes.txt next to this script."
            )
            self.jokes = []

        self.current_setup = tk.StringVar(value="Press the button to hear a joke!")
        self.current_punchline = tk.StringVar(value="")
        self.last_index = None

        self.build_widgets()

    def setup_styles(self):
        """Configure custom button themes."""
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Accent.TButton",
            background="#f59e0b",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=(18, 9),
        )
        style.configure(
            "Secondary.TButton",
            background="#e2e8f0",
            foreground="#0f172a",
            font=("Segoe UI", 10, "bold"),
            padding=(16, 9),
        )
        style.configure(
            "Danger.TButton",
            background="#ef4444",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 9),
        )

        style.map("Accent.TButton", background=[("active", "#fbbf24"), ("pressed", "#d97706")])
        style.map("Secondary.TButton", background=[("active", "#cbd5e1"), ("pressed", "#94a3b8")])
        style.map("Danger.TButton", background=[("active", "#f87171"), ("pressed", "#dc2626")])

    def build_widgets(self):
        """Create and arrange all UI elements."""
        main = tk.Frame(self, bg="#0b1020", padx=24, pady=22)
        main.pack(fill="both", expand=True)

        # Top header banner
        header = tk.Frame(main, bg="#172554", padx=22, pady=18)
        header.pack(fill="x", pady=(0, 16))
        tk.Label(
            header, text="ALEXA", bg="#172554", fg="#38bdf8",
            font=("Segoe UI", 32, "bold")
        ).pack()
        tk.Label(
            header, text="JOKE ASSISTANT", bg="#172554", fg="#ffffff",
            font=("Segoe UI", 15, "bold")
        ).pack(pady=(0, 4))
        tk.Label(
            header, text="Your little break for a big laugh",
            bg="#172554", fg="#cbd5e1", font=("Segoe UI", 10)
        ).pack()

        # Button control bar
        controls = tk.Frame(main, bg="#0b1020")
        controls.pack(fill="x", pady=(0, 14))

        self.ask_btn = ttk.Button(
            controls, text="Tell me a joke",
            command=self.tell_joke, style="Accent.TButton"
        )
        self.ask_btn.pack(side="left", padx=(0, 8))

        self.punchline_btn = ttk.Button(
            controls, text="Show punchline",
            command=self.show_punchline, state="disabled",
            style="Secondary.TButton"
        )
        self.punchline_btn.pack(side="left", padx=(0, 8))

        self.next_btn = ttk.Button(
            controls, text="Next joke",
            command=self.tell_joke, style="Secondary.TButton"
        )
        self.next_btn.pack(side="left")

        ttk.Button(
            controls, text="Quit",
            command=self.destroy, style="Danger.TButton"
        ).pack(side="right")

        # Main joke card
        display = tk.Frame(
            main, bg="#ffffff", padx=24, pady=20,
            highlightthickness=1, highlightbackground="#dbeafe"
        )
        display.pack(fill="both", expand=True)

        tk.Label(
            display, text="YOUR JOKE", bg="#ffffff", fg="#64748b",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(4, 18))

        tk.Label(
            display, textvariable=self.current_setup, wraplength=620,
            justify="center", bg="#ffffff", fg="#0f172a",
            font=("Segoe UI", 17, "bold")
        ).pack(pady=(0, 12))

        tk.Label(
            display, textvariable=self.current_punchline, wraplength=620,
            justify="center", bg="#ffffff", fg="#0369a1",
            font=("Segoe UI", 13, "italic")
        ).pack(pady=(0, 10))

    def tell_joke(self):
        """Pick a random joke without repeating the previous one."""
        try:
            self.jokes = load_jokes(DATA_FILE)
        except (OSError, UnicodeDecodeError) as error:
            messagebox.showerror(
                "Could Not Load Jokes",
                f"Could not read {DATA_FILE}: {error}"
            )
            self.jokes = []

        if not self.jokes:
            messagebox.showinfo("No Jokes", "No jokes could be loaded from randomJokes.txt.")
            return

        index = random.randrange(len(self.jokes))
        while len(self.jokes) > 1 and index == self.last_index:
            index = random.randrange(len(self.jokes))
        self.last_index = index

        setup, _ = self.jokes[index]
        self.current_setup.set(setup)
        self.current_punchline.set("")
        self.punchline_btn.config(state="normal")

    def show_punchline(self):
        """Reveal the punchline for the current joke."""
        if self.last_index is None or not self.jokes:
            return

        _, punchline = self.jokes[self.last_index]
        self.current_punchline.set(punchline)
        self.punchline_btn.config(state="disabled")


if __name__ == "__main__":
    app = JokeApp()
    app.mainloop()