import customtkinter as ctk
import threading

from tkinter import filedialog
from lyricsfetcher import lyrics


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("theme/purple.json") # prefer #6f00de


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Song2SRT")
        self.geometry("850x750")


        self.entry = ctk.CTkEntry(self, placeholder_text="Song name or artist")
        self.entry.pack(pady=10, padx=20, fill="x")
        self.entry.bind("<Return>", self.start_search)


        self.botao = ctk.CTkButton(self, text="Search", command=self.start_search)
        self.botao.pack(pady=10, padx=20)


        self.scroll = ctk.CTkScrollableFrame(self, label_text="Results")
        self.scroll.pack(pady=10, padx=20, fill="both", expand=True)
        self.scroll._parent_canvas.bind("<Enter>", lambda e: self._activate_canvas_scroll())
        self.scroll._parent_canvas.bind("<Leave>", lambda e: self._deactivate_scroll())
        

        self.status = ctk.CTkLabel(self, text="")
        self.status.pack(pady=5)


        self.text_box = ctk.CTkTextbox(self, height=200)
        self.text_box.pack(padx=20, pady=10, fill="both", expand=False)

        self.save_button = ctk.CTkButton(
            self,
            text="Download lrc file",
            command=self.generate_lrc,
            state="disabled",
        )
        self.save_button.pack(pady=(0, 15))


        self.unbind_all("<Button-4>")
        self.unbind_all("<Button-5>")
        self.unbind_all("<MouseWheel>")
        self.bind_all("<Button-4>", lambda e: self._universal_scroll_handler(e, -1))
        self.bind_all("<Button-5>", lambda e: self._universal_scroll_handler(e, 1))
        self.bind_all("<MouseWheel>", self._universal_scroll_handler)

    def _is_descendant(self, widget, ancestor):
        try:
            if widget is None or ancestor is None:
                return False
            anc_name = ancestor._w
            w = widget
            while True:
                if getattr(w, "_w", None) == anc_name:
                    return True
                parent_name = w.winfo_parent()
                if not parent_name:
                    return False
                w = self.nametowidget(parent_name)
        except Exception:
            return False

    def _universal_scroll_handler(self, event, forced_direction=None):
        try:
            widget_under = self.winfo_containing(event.x_root, event.y_root)
            if not widget_under:
                return
            if forced_direction is not None:
                delta = forced_direction
            else:
                raw = getattr(event, "delta", 0)
                delta = -1 if raw > 0 else 1
            if self._is_descendant(widget_under, self.scroll):
                self.scroll._parent_canvas.yview_scroll(delta, "units")
                return
            if self._is_descendant(widget_under, self.text_box):
                self.text_box.yview_scroll(delta, "units")
                return
        except Exception:
            pass



    def start_search(self, event=None):
        term = self.entry.get().strip()
        if not term:
            return

        self.status.configure(text="Searching...")
        self.clean_results()
        threading.Thread(target=self.make_search, args=(term,), daemon=True).start()

    def make_search(self, term):
        results = lyrics.fetcher(term)
        self.after(0, lambda: self.show_results(results))

    def show_results(self, results):
        self.clean_results()
        if not results:
            self.status.configure(text="Nothing was found.")
            return

        self.status.configure(text=f"{len(results)} results found:")
        for item in results:
            texto = f"{item['titulo']} — {item['artista']}"
            button = ctk.CTkButton(
                self.scroll,
                text=texto,
                anchor="w",
                command=lambda i=item['id']: self.start_lyrics_search(i)
            )
            button.pack(fill="x", pady=2, padx=5)

    def start_lyrics_search(self, track_id):
        self.status.configure(text="Fetching lyrics...")
        self.text_box.delete("1.0", "end")
        threading.Thread(target=self.fetch_lyrics, args=(track_id,), daemon=True).start()

    def fetch_lyrics(self, track_id):
        lyric = lyrics.search_lyrics(track_id)
        self.after(0, lambda: self.show_lyrics(lyric))

    def show_lyrics(self, lyric):
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", lyric)
        self.status.configure(text="Lyrics loaded ✅")
        self.save_button.configure(state="normal")
        self.current_lyrics = lyric

    def clean_results(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()



    def generate_lrc(self):
        if not hasattr(self, "current_lyrics") or not self.current_lyrics:
            self.status.configure(text="No lyrics loaded.")
            return

        lines = [line.strip() for line in self.current_lyrics.split("\n") if line.strip()]
        lrc_text = "\n".join(lines)

        filename = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".lrc",
            filetypes=[("LRC files", "*.lrc"), ("All files", "*.*")],
            title="Save LRC file as",
            initialdir="~",
        )
        if not filename:
            self.status.configure(text="Canceled.")
            return

        with open(filename, "w", encoding="utf-8") as f:
            f.write(lrc_text)

        self.status.configure(text=f"LRC saved in: {filename}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
