import tkinter as tk
from Controllers.face_controller import FaceController

class FaceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Emócie NICO-HEAD")
        self.controller = FaceController()
        self.emotions = self.controller.get_emotions() 
        self.create_widgets()
        self.controller.turn_part("ON", "ALL")

    def create_widgets(self):
        if not self.emotions:
            label = tk.Label(self.root, text="Žiadne emócie nie sú dostupné.")
            label.pack(pady=10)
            return
        label = tk.Label(self.root, text="Vyber emóciu:")
        label.pack(pady=10)
        for emotion in self.emotions:
            btn = tk.Button(self.root, text=emotion, width=20, command=lambda e=emotion: self.controller.execute_emotion(e))
            btn.pack(pady=5)
        
        stop_btn = tk.Button(self.root, text="Stop Emotion", width=20, command=self.controller.stop_emotion)
        stop_btn.pack(pady=10)

    def on_close(self):
        self.controller.turn_part("OFF", "ALL")
        self.controller.close_connection()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
