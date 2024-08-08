import tkinter as tk
from tkinter import ttk


class KMPVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KMP Algorithm Visualizer")
        self.geometry("1200x800")

        # Initial texts
        self.text = "ABABDABABCABABABACDABABCABAB"
        self.pattern = "ABABCABAB"

        # Initialize variables for LPS and KMP
        self.lps = [0] * len(self.pattern)
        self.step = 0

        # Setup the GUI
        self.setup_frames()
        self.display_texts()
        self.create_buttons()

    def setup_frames(self):
        self.text_frame = ttk.LabelFrame(self, text="Text", height=100)
        self.text_frame.pack(fill="x", padx=10, pady=10)

        self.pattern_frame = ttk.LabelFrame(self, text="Pattern", height=100)
        self.pattern_frame.pack(fill="x", padx=10, pady=10)

        self.lps_frame = ttk.LabelFrame(self, text="LPS Array", height=100)
        self.lps_frame.pack(fill="x", padx=10, pady=10)

        self.status_frame = ttk.LabelFrame(self, text="Status", height=200)
        self.status_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.status_canvas = tk.Canvas(self.status_frame)
        self.status_canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(
            self.status_frame, orient="vertical", command=self.status_canvas.yview
        )
        self.scrollbar.pack(side="right", fill="y")

        self.status_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.status_canvas.bind(
            "<Configure>",
            lambda e: self.status_canvas.configure(
                scrollregion=self.status_canvas.bbox("all")
            ),
        )

        self.status_content = tk.Frame(self.status_canvas)
        self.status_canvas.create_window(
            (0, 0), window=self.status_content, anchor="nw"
        )

        self.status_label = tk.Label(
            self.status_content, text="", font=("Courier", 14), justify="left"
        )
        self.status_label.pack(padx=10, pady=10)

    def display_texts(self):
        self.text_label = tk.Label(
            self.text_frame, text=self.text, font=("Courier", 16)
        )
        self.text_label.pack(padx=10, pady=10)

        self.pattern_label = tk.Label(
            self.pattern_frame, text=self.pattern, font=("Courier", 16)
        )
        self.pattern_label.pack(padx=10, pady=10)

        self.lps_label = tk.Label(
            self.lps_frame,
            text="LPS: " + " ".join(map(str, self.lps)),
            font=("Courier", 16),
        )
        self.lps_label.pack(padx=10, pady=10)

    def create_buttons(self):
        self.lps_button = ttk.Button(
            self.status_frame, text="Compute LPS Step", command=self.compute_lps_step
        )
        self.lps_button.pack(side="left", padx=10, pady=10)

        self.search_button = ttk.Button(
            self.status_frame,
            text="Search Pattern Step",
            command=self.search_pattern_step,
            state="disabled",
        )
        self.search_button.pack(side="left", padx=10, pady=10)

        self.reset_button = ttk.Button(
            self.status_frame, text="Reset", command=self.reset
        )
        self.reset_button.pack(side="left", padx=10, pady=10)

    def reset(self):
        self.lps = [0] * len(self.pattern)
        self.step = 0
        self.display_texts()
        self.lps_button.config(state="normal")
        self.search_button.config(state="disabled")
        self.update_status("")

    def compute_lps_step(self):
        if self.step == 0:
            self.prevLPS = 0
            self.i = 1
            self.step += 1
            self.update_status("Starting LPS computation...")
            self.update_lps_label()
            self.update_pattern_label()
        elif self.i < len(self.pattern):
            if self.pattern[self.i] == self.pattern[self.prevLPS]:
                self.prevLPS += 1
                self.lps[self.i] = self.prevLPS
                self.i += 1
                self.update_status(
                    f"LPS[{self.i-1}] = {self.prevLPS} because pattern[{self.i-1}] == pattern[{self.prevLPS-1}]"
                )
                self.update_status(
                    f"prevLPS was {self.prevLPS - 1} and so now I assign prevLPS + 1 = {self.prevLPS}"
                )
            elif self.prevLPS == 0:
                self.lps[self.i] = 0
                self.i += 1
                self.update_status(
                    f"LPS[{self.i-1}] = 0 because no proper prefix which is also suffix"
                )
            else:
                self.update_status(
                    f"Backtrack prevLPS from {self.prevLPS} to prevLPS = LPS[prevLPS - 1] = {self.lps[self.prevLPS - 1]}\nbecause pattern[{self.i}] != pattern[{self.prevLPS}]"
                )
                self.prevLPS = self.lps[self.prevLPS - 1]
            self.update_pattern_label()
            self.update_lps_label()
        else:
            self.update_status("LPS computation complete!")
            self.lps_button.config(state="disabled")
            self.search_button.config(state="normal")

    def update_lps_label(self):
        lps_text = "LPS: " + " ".join(map(str, self.lps))
        highlighted_text = ""
        for index, char in enumerate(lps_text):
            if index == self.i * 2 + 5:
                highlighted_text += "["
            if index == self.i * 2 + 7:
                highlighted_text += "]"
            highlighted_text += char
        # Add prevLPS pointer
        if self.prevLPS >= 0:
            prevLPS_index = self.prevLPS * 2 + 5
            highlighted_text = (
                highlighted_text[:prevLPS_index]
                + "("
                + highlighted_text[prevLPS_index : prevLPS_index + 1]
                + ")"
                + highlighted_text[prevLPS_index + 1 :]
            )
        self.lps_label.config(text=highlighted_text)

    def update_pattern_label(self):
        pattern_text = ""
        for index, char in enumerate(self.pattern):
            if index == self.i:
                pattern_text += f"[{char}]"
            elif index == self.prevLPS:
                pattern_text += f"({char})"
            else:
                pattern_text += char
        self.pattern_label.config(text=pattern_text)

    def update_text_label(self):
        text_text = self.text
        highlighted_text = ""
        for index, char in enumerate(text_text):
            if index == self.i:
                highlighted_text += "["
            highlighted_text += char
            if index == self.i:
                highlighted_text += "]"
        self.text_label.config(text=highlighted_text)

    def update_pattern_label_search(self):
        pattern_text = self.pattern
        highlighted_text = ""
        for index, char in enumerate(pattern_text):
            if index == self.j:
                highlighted_text += "["
            highlighted_text += char
            if index == self.j:
                highlighted_text += "]"
        self.pattern_label.config(text=highlighted_text)

    def update_match_label(self):
        match_text = " " * self.i + self.pattern
        self.match_label.config(text=match_text)

    def search_pattern_step(self):
        if self.step == 1:
            self.i = 0
            self.j = 0
            self.step += 1
            self.start = len(self.text)
            self.res = []
            self.update_status("Starting pattern search...")
        elif self.i < len(self.text):
            if self.j >= len(self.pattern):
                self.res.append((self.start, self.i - 1))
                self.update_status(
                    f"Pattern found from index {self.start} to {self.i-1}"
                )
                self.j = self.lps[self.j - 1]
                self.start = len(self.text)
            elif self.text[self.i] == self.pattern[self.j]:
                self.start = min(self.start, self.i)
                self.j += 1
                self.i += 1
                self.update_status(f"Match at text[{self.i-1}] and pattern[{self.j-1}]")
            elif self.j > 0:
                self.update_status(
                    f"Backtrack j from {self.j} to {self.lps[self.j - 1]}"
                )
                self.j = self.lps[self.j - 1]
            else:
                self.i += 1
                self.start = self.i
                self.update_status(f"Mismatch, moving to text[{self.i}]")
            self.update_text_label()
            self.update_pattern_label_search()
            self.update_match_label()
        else:
            if self.i - self.start == len(self.pattern):
                self.res.append((self.start, self.i - 1))
                self.update_status(
                    f"Pattern found from index {self.start} to {self.i-1}"
                )
            self.display_results()
            self.search_button.config(state="disabled")
            self.update_status("Pattern search complete!")

    def update_status(self, message):
        current_status = self.status_label.cget("text")
        self.status_label.config(text=current_status + "\n" + message)

    def display_results(self):
        self.update_status(
            "Pattern found at indices: "
            + ", ".join([f"({start}, {end})" for start, end in self.res])
        )


if __name__ == "__main__":
    app = KMPVisualizer()
    app.mainloop()
