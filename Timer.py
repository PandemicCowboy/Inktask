import tkinter as tk
from PIL import Image, ImageTk

def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02}:{secs:02}"

class Task:
    def __init__(self, master, name, duration_minutes):
        self.frame = tk.Frame(master, bg="#f6f2e7", bd=2, relief="ridge")
        self.name = name
        self.duration = duration_minutes * 60
        self.remaining = self.duration
        self.running = False

        self.label = tk.Label(self.frame, text=name,
                              font=("Georgia", 14, "italic"), bg="#f6f2e7", fg="#2a2a2a")
        self.label.pack(padx=10, pady=(5, 2))

        self.timer_label = tk.Label(self.frame, text=format_time(self.remaining),
                                    font=("Georgia", 12), bg="#f6f2e7", fg="#555555")
        self.timer_label.pack()

        self.status_label = tk.Label(self.frame, text="",
                                     font=("Georgia", 12), bg="#f6f2e7", fg="green")
        self.status_label.pack()

        button_frame = tk.Frame(self.frame, bg="#f6f2e7")
        button_frame.pack(pady=5)

        self.start_button = tk.Button(button_frame, text="✒ Start", command=self.start_timer,
                                      bg="#dcd6c4", font=("Georgia", 10))
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(button_frame, text="✒ Pause", command=self.pause_timer,
                                      bg="#dcd6c4", font=("Georgia", 10))
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.frame.pack(pady=8, fill="x")

    def start_timer(self):
        if not self.running and self.remaining > 0:
            self.running = True
            self.count_down()

    def pause_timer(self):
        self.running = False

    def count_down(self):
        if self.running and self.remaining > 0:
            self.remaining -= 1
            self.timer_label.config(text=format_time(self.remaining))
            self.frame.after(1000, self.count_down)
        elif self.remaining == 0:
            self.running = False
            self.timer_label.config(text="00:00")
            self.status_label.config(text="✔ Completed")

class InkApp:
    def __init__(self, root):
        root.title("🖋️ InkTask — Daily Tracker")
        root.geometry("800x600")
        root.resizable(False, False)

        try:
            bg_image = Image.open("parchment.png").resize((800, 600))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            canvas = tk.Canvas(root, width=800, height=600)
            canvas.pack(fill="both", expand=True)
            canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
        except Exception as e:
            print("Image loading error:", e)
            canvas = tk.Canvas(root, bg="#f6f2e7", width=800, height=600)
            canvas.pack(fill="both", expand=True)

        self.content_frame = tk.Frame(canvas, bg="#f6f2e7")
        canvas.create_window(10, 10, anchor="nw", window=self.content_frame)

        title = tk.Label(self.content_frame, text="🖋️ InkTask — Daily Tracker",
                         font=("Georgia", 20, "bold"), bg="#f6f2e7", fg="#000000")
        title.pack(pady=15)

        self.task_container = tk.Frame(self.content_frame, bg="#f6f2e7")
        self.task_container.pack()

        self.add_task_ui()

    def add_task_ui(self):
        entry_frame = tk.Frame(self.content_frame, bg="#f6f2e7")
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="Task:", font=("Georgia", 12), bg="#f6f2e7").grid(row=0, column=0)
        self.name_entry = tk.Entry(entry_frame, font=("Georgia", 12), width=25)
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Label(entry_frame, text="Duration (min):", font=("Georgia", 12), bg="#f6f2e7").grid(row=1, column=0)
        self.duration_entry = tk.Entry(entry_frame, font=("Georgia", 12), width=10)
        self.duration_entry.grid(row=1, column=1, padx=5)

        add_button = tk.Button(entry_frame, text="Add Task", command=self.add_task,
                               bg="#dcd6c4", font=("Georgia", 10))
        add_button.grid(row=2, column=0, columnspan=2, pady=8)

    def add_task(self):
        name = self.name_entry.get()
        try:
            duration = int(self.duration_entry.get())
            Task(self.task_container, name, duration)
        except ValueError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = InkApp(root)
    root.mainloop()