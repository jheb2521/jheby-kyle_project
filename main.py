import tkinter as tk
from tkinter import ttk

# Small Tkinter app that visually approximates the QUPAL chat UI from the screenshot.
# Uses only the Python standard library (tkinter). No external assets required.

class QuPalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QUPAL — Thrift Shopping Assistant")
        self.geometry("1200x768")
        self.configure(bg="#f6fbfb")

        self._create_styles()
        self._create_header()
        self._create_chat_area()
        self._create_input_bar()

    def _create_styles(self):
        style = ttk.Style(self)
        # Use default theme and set some colors
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Header.TFrame", background="#e8fbfb")
        style.configure("Logo.TLabel", background="#e8fbfb", font=("Helvetica", 14, "bold"))
        style.configure("Title.TLabel", background="#e8fbfb", font=("Helvetica", 10), foreground="#6a6a6a")

    def _create_header(self):
        header = ttk.Frame(self, style="Header.TFrame", height=80)
        header.pack(fill=tk.X, side=tk.TOP)

        left = tk.Frame(header, bg="#e8fbfb")
        left.pack(side=tk.LEFT, padx=20, pady=12)

        # Logo circle drawn on a small canvas
        logo_canvas = tk.Canvas(left, width=56, height=56, highlightthickness=0, bg="#e8fbfb")
        logo_canvas.create_oval(4, 4, 52, 52, fill="#6fe6e6", outline="")
        # simple robot eyes/antenna
        logo_canvas.create_rectangle(22,22,34,30, fill="#ffffff", outline="")
        logo_canvas.create_oval(28,12,34,18, fill="#ffffff", outline="")
        logo_canvas.pack(side=tk.LEFT)

        text_frame = tk.Frame(left, bg="#e8fbfb")
        text_frame.pack(side=tk.LEFT, padx=12)
        title = ttk.Label(text_frame, text="QUPAL", style="Logo.TLabel")
        title.pack(anchor=tk.W)
        subtitle = ttk.Label(text_frame, text="Your Thrift Shopping Assistant", style="Title.TLabel")
        subtitle.pack(anchor=tk.W)

    def _create_chat_area(self):
        # Main chat area with a single example message bubble
        chat_frame = tk.Frame(self, bg="#f6fbfb")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=(8,6))

        # large white-ish card area to hold messages
        card = tk.Frame(chat_frame, bg="#ffffff", bd=0)
        card.place(relwidth=0.96, relheight=0.9, relx=0.02, rely=0.02)

        # Example message bubble (left-aligned)
        bubble_canvas = tk.Canvas(card, bg="#ffffff", highlightthickness=0)
        bubble_canvas.pack(padx=20, pady=24, anchor="nw")

        msg = ("Hello! I'm QUPAL, your thrift shopping AI assistant. I can help you find amazing\n"
               "second-hand treasures, identify vintage items, estimate values, and give tips on\n"
               "thrifting. What are you looking for today?")

        # Draw rounded rectangle bubble
        x0, y0 = 6, 6
        width = 760
        # compute text height using a hidden text widget to wrap nicely
        text_item = bubble_canvas.create_text(x0 + 12, y0 + 12, anchor="nw", width=width-40,
                                              text=msg, font=("Helvetica", 11), fill="#3b3b3b")
        bbox = bubble_canvas.bbox(text_item)
        if bbox:
            x1 = bbox[2] + 20
            y1 = bbox[3] + 12
        else:
            x1 = width
            y1 = 80

        radius = 14
        # Draw rounded rectangle background for the bubble
        self._round_rect(bubble_canvas, x0, y0, x1, y1, radius, fill="#f0fdff", outline="")
        # Move text to be on top of rounded rect
        bubble_canvas.lift(text_item)

        # Tiny assistant icon on the left of the bubble
        bubble_canvas.create_oval(x0-36, y0+6, x0-6, y0+36, fill="#6fe6e6", outline="")
        bubble_canvas.create_text(x0-21, y0+20, text="Q", font=("Helvetica", 12, "bold"), fill="#ffffff")

    def _round_rect(self, canvas, x1, y1, x2, y2, r=25, **kwargs):
        # Draws a rounded rectangle on the given canvas
        points = [
            x1+r, y1,
            x1+r, y1,
            x2-r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y1+r,
            x2, y2-r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x2-r, y2,
            x1+r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y2-r,
            x1, y1+r,
            x1, y1+r,
            x1, y1,
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    def _create_input_bar(self):
        bar = tk.Frame(self, bg="#f6fbfb", height=80)
        bar.pack(fill=tk.X, side=tk.BOTTOM)

        import tkinter as tk
        from tkinter import ttk
        import os
        import threading


        class QuPalApp(tk.Tk):
            """Resizable chat UI with message stacking and a simple rule-based bot responder.

            The app will attempt to use a local rule-based responder. If you set
            the environment variable `OPENAI_API_KEY` and have the `openai` package
            installed, the app will try to use OpenAI (optional).
            """

            def __init__(self):
                super().__init__()
                self.title("QUPAL — Thrift Shopping Assistant")
                self.geometry("1200x768")
                self.configure(bg="#f6fbfb")

                self._create_styles()
                self._create_header()
                self._create_chat_area()
                self._create_input_bar()

                # initial assistant greeting
                self.add_message(
                    "Hello! I'm QUPAL, your thrift shopping AI assistant. I can help you find amazing second-hand treasures, identify vintage items, estimate values, and give tips on thrifting. What are you looking for today?",
                    sender="assistant",
                )

            def _create_styles(self):
                style = ttk.Style(self)
                try:
                    style.theme_use("clam")
                except Exception:
                    pass

            def _create_header(self):
                header = tk.Frame(self, bg="#e8fbfb", height=80)
                header.pack(fill=tk.X, side=tk.TOP)

                left = tk.Frame(header, bg="#e8fbfb")
                left.pack(side=tk.LEFT, padx=20, pady=12)

                logo_canvas = tk.Canvas(left, width=56, height=56, highlightthickness=0, bg="#e8fbeb")
                logo_canvas.create_oval(4, 4, 52, 52, fill="#6fe6e6", outline="")
                logo_canvas.create_rectangle(22, 22, 34, 30, fill="#ffffff", outline="")
                logo_canvas.pack(side=tk.LEFT)

                text_frame = tk.Frame(left, bg="#e8fbeb")
                text_frame.pack(side=tk.LEFT, padx=12)
                tk.Label(text_frame, text="QUPAL", bg="#e8fbeb", font=("Helvetica", 14, "bold")).pack(anchor=tk.W)
                tk.Label(text_frame, text="Your Thrift Shopping Assistant", bg="#e8fbeb", font=("Helvetica", 10), fg="#6a6a6a").pack(anchor=tk.W)

            def _create_chat_area(self):
                # Chat area: white card with scrollable message stack
                container = tk.Frame(self, bg="#f6fbfb")
                container.pack(fill=tk.BOTH, expand=True, padx=18, pady=(8, 6))

                card = tk.Frame(container, bg="#ffffff")
                card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

                # Canvas + scrollbar to hold a vertical messages frame
                self.canvas = tk.Canvas(card, bg="#ffffff", highlightthickness=0)
                self.scrollbar = tk.Scrollbar(card, orient=tk.VERTICAL, command=self.canvas.yview)
                self.canvas.configure(yscrollcommand=self.scrollbar.set)
                self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                # The frame inside the canvas that will contain the message widgets
                self.messages_frame = tk.Frame(self.canvas, bg="#ffffff")
                self.canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")

                # Make resizing behave: update scrollregion when the size changes
                self.messages_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
                self.canvas.bind("<Configure>", self._on_canvas_configure)

            def _on_canvas_configure(self, event):
                # Keep the inner frame width synced with the canvas width
                canvas_width = event.width
                # find the canvas window item and set its width
                # note: itemconfig expects the item id; here the window has id 1 since it's the first created
                try:
                    self.canvas.itemconfig(1, width=canvas_width)
                except Exception:
                    pass

            def _create_input_bar(self):
                bar = tk.Frame(self, bg="#f6fbfb", height=80)
                bar.pack(fill=tk.X, side=tk.BOTTOM)

                inner = tk.Frame(bar, bg="#f6fbfb")
                inner.pack(fill=tk.X, padx=22, pady=12)

                entry_bg = tk.Frame(inner, bg="#ffffff")
                entry_bg.pack(side=tk.LEFT, fill=tk.X, expand=True)

                self.entry_var = tk.StringVar()
                self.entry = tk.Entry(entry_bg, textvariable=self.entry_var, bd=0, font=("Helvetica", 11))
                self.entry.pack(fill=tk.X, padx=12, pady=12)
                self.entry.insert(0, "Type your message...")
                self.entry.bind("<FocusIn>", self._clear_placeholder)
                self.entry.bind("<Return>", lambda e: self._on_send())

                send_btn = tk.Canvas(inner, width=56, height=56, bg="#f6fbfb", highlightthickness=0)
                send_btn.pack(side=tk.RIGHT, padx=(12, 0))
                send_btn.create_oval(4, 4, 52, 52, fill="#6fe6e6", outline="")
                send_btn.create_polygon(20, 18, 40, 28, 22, 34, fill="#ffffff", outline="")
                send_btn.bind("<Button-1>", lambda e: self._on_send())

            def _clear_placeholder(self, event=None):
                if self.entry.get() == "Type your message...":
                    self.entry.delete(0, tk.END)

            def add_message(self, text, sender="assistant"):
                """Add a message bubble to the messages_frame.

                sender: 'assistant' or 'user'
                """
                # Container frame for this message
                bubble_frame = tk.Frame(self.messages_frame, bg="#ffffff", pady=6)
                bubble_frame.pack(fill=tk.X, anchor="w")

                # Determine bubble appearance
                wrap = 760
                if sender == "assistant":
                    bg = "#f0fdff"
                    anchor = "w"
                    side = tk.LEFT
                    padx = (12, 200)
                else:
                    bg = "#e9e9e9"
                    anchor = "e"
                    side = tk.RIGHT
                    padx = (200, 12)

                inner = tk.Frame(bubble_frame, bg="#ffffff")
                inner.pack(fill=tk.X)
                # bubble holder with padding to create left/right alignment
                holder = tk.Frame(inner, bg="#ffffff")
                holder.pack(fill=tk.X, padx=padx)

                bubble = tk.Label(holder, text=text, bg=bg, justify=tk.LEFT, wraplength=wrap, padx=12, pady=8, font=("Helvetica", 11))
                bubble.pack(side=side, anchor=anchor)

                # After adding a message, scroll to the bottom
                self.after(50, lambda: self.canvas.yview_moveto(1.0))

            def _on_send(self):
                text = self.entry_var.get().strip()
                if not text or text == "Type your message...":
                    return
                # add user message
                self.add_message(text, sender="user")
                self.entry_var.set("")

                # get bot response in a short background thread (simulated processing)
                threading.Thread(target=self._respond_to_user, args=(text,), daemon=True).start()

            def _respond_to_user(self, user_text):
                # Try optional OpenAI responder first if configured
                response = None
                api_key = os.environ.get("OPENAI_API_KEY")
                if api_key:
                    try:
                        import openai

                        openai.api_key = api_key
                        # simple completion call if openai package is available
                        completion = openai.Completion.create(
                            engine="text-davinci-003",
                            prompt=f"You are a helpful thrift-shopping assistant. Reply concisely to: {user_text}",
                            max_tokens=150,
                        )
                        response = completion.choices[0].text.strip()
                    except Exception:
                        # fall back to rule-based on any error
                        response = None

                if not response:
                    response = self._rule_based_response(user_text)

                # Schedule UI update on main thread
                self.after(100, lambda: self.add_message(response, sender="assistant"))

            def _rule_based_response(self, text):
                t = text.lower()
                if any(x in t for x in ["hello", "hi", "hey"]):
                    return "Hi there! What kind of thrift item are you looking for?"
                if "vintage" in t or "identify" in t or "what is this" in t:
                    return "Tell me a bit about the item's markings, materials, and any labels — I can help identify it."
                if "value" in t or "estimate" in t or "worth" in t:
                    return "I can give a rough estimate if you tell me the brand, condition, and approximate age."
                if "tips" in t or "thrift" in t:
                    return "Look for solid construction, classic brands, and minimal staining — always inspect seams and zippers."
                if "bye" in t or "thanks" in t:
                    return "You're welcome — happy thrifting!"
                # fallback small talk
                return "I don't have an exact answer for that, but I can help if you give more details."


        if __name__ == "__main__":
            app = QuPalApp()
            app.mainloop()
