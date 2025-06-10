import os, time
import tkinter as tk
from math import cos, sin, radians
from PIL import Image, ImageGrab, ImageTk

class StickFigureApp:
    def __init__(self, root, generated_images_dir):
        self.root = root
        self.root.title("Generator vizualnych emocii")

        self.generated_images_dir = generated_images_dir
        os.makedirs(self.generated_images_dir, exist_ok=True)

        self.canvas = tk.Canvas(root, width=1000, height=1000, bg="white")
        self.canvas.grid(row=0, column=0)

        control_frame = tk.Frame(root)
        control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        smile_mouth = [
            [20, -20, 20, -20],
            [30, -30, 20, -20],
            [30, -30, 30, -30],
            [40, -40, 30, -30],
            [40, -40, 40, -40]
        ]

        sad_mouth = [
            [0, 0, -10, 10],
            [-10, 10, -10, 10],
            [-20, 20, -10, 10],
            [-20, 20, -20, 20],
            [-30, 30, -20, 20],
            [-30, 30, -30, 30],
            [-40, 40, -30, 30]
        ]

        open_mouth = [
            [-20, 20, 20, -20],
            [-30, 30, 20, -20],
            [-30, 30, 30, -30],
            [-40, 40, 30, -30],
            [-40, 40, 40, -40]                
        ]
        disgust_mouth = [
            [-20, 20, 5, -5],
            [5, -5, -5, 5]
        ]
        neutral_mouth =  [
            [0, 0, 0, 0],
            [-10, 10, 10, -10],
            [-10, 10, 0, 0],
            [0, 0, 10, -10]
        ]

        normal_brows = [
            [0, 0],
            [3, -3],
            [-3, 3]
        ]

        up_brows = [
            [-5, 5],
            [-10, 10],
            [-15, 15],
            [-20, 20]
        ]

        down_brows = [
            [5, -5],
            [10, -10],
            [15, -15],
            [20, -20]
        ]

        def combine_mouth_brows(mouth_list, brows_list):
            return [
            mouth + brows
                for mouth in mouth_list
                    for brows in brows_list
            ]

        self.emotion_rotations = {
            "happy": [
            ["normal.jpg", "fully_open.jpg"],
            combine_mouth_brows(smile_mouth, up_brows)
            ],
            "sad": [
            ["normal.jpg", "half_way.jpg"],
            combine_mouth_brows(sad_mouth, up_brows)
            ],
            "angry": [
            ["half_way.jpg"],
            combine_mouth_brows(sad_mouth, down_brows)
            ],
            "disgust": [
            ["normal.jpg"],
            combine_mouth_brows(disgust_mouth, down_brows)
            ],
            "surprise": [
            ["fully_open.jpg"],
            combine_mouth_brows(open_mouth, up_brows)
            ],
            "scared": [
            ["fully_open.jpg"],
            combine_mouth_brows(neutral_mouth + sad_mouth, up_brows)
            ],
            "neutral": [
            ["closed.jpg", "normal.jpg"],
            combine_mouth_brows(neutral_mouth, normal_brows)
            ],
        }

        self.points = {}
        default_points = {
            1: (450, 775),
            2: (550, 775),
            3: (440, 840),
            4: (560, 840),
            5: (350, 430),
            6: (650, 430)
        }

        arms_text = ["Ústa UL", "Ústa UR", "Ústa LL", "Ústa LR", "Obočie L", "Obočie R"]

        for i in range(1, 7):
            tk.Label(control_frame, text=f"{arms_text[i-1]} (x, y):").grid(row=i-1, column=0, sticky="w")
            x_var = tk.IntVar(value=default_points[i][0])
            y_var = tk.IntVar(value=default_points[i][1])
            self.points[i] = (x_var, y_var)
            tk.Entry(control_frame, textvariable=x_var, width=5).grid(row=i-1, column=1)
            tk.Entry(control_frame, textvariable=y_var, width=5).grid(row=i-1, column=2)

        self.left_lengths = {}
        self.right_lengths = {}
        left_defaults = {1: 40, 2: 40, 3: 50, 4: 40, 5: 100, 6: 75}
        right_defaults = {1: 40, 2: 40, 3: 40, 4: 50, 5: 75, 6: 100}

        for i in range(1, 7):
            tk.Label(control_frame, text=f"L-{arms_text[i-1]}:").grid(row=6+i, column=0, sticky="w")
            left_length_var = tk.IntVar(value=left_defaults[i])
            self.left_lengths[i] = left_length_var
            tk.Entry(control_frame, textvariable=left_length_var, width=5).grid(row=6+i, column=1)

            tk.Label(control_frame, text=f"R-{arms_text[i-1]}:").grid(row=6+i, column=2, sticky="w")
            right_length_var = tk.IntVar(value=right_defaults[i])
            self.right_lengths[i] = right_length_var
            tk.Entry(control_frame, textvariable=right_length_var, width=5).grid(row=6+i, column=3)

        self.angles = {}

        for i in range(1, 7):
            tk.Label(control_frame, text=f"{arms_text[i-1]} (°):").grid(row=13+i, column=0, sticky="w")
            angle_var = tk.IntVar(value=0)
            self.angles[i] = angle_var
            tk.Scale(control_frame, from_=-180, to=180, orient="horizontal", variable=angle_var, length=150).grid(row=13+i, column=1, columnspan=3)

        tk.Label(control_frame, text="Arm thickness:").grid(row=21, column=0, sticky="w", pady=5)
        self.line_thickness = tk.IntVar(value=3)
        tk.Scale(control_frame, from_=1, to=10, orient="horizontal", variable=self.line_thickness, length=150).grid(row=21, column=1, columnspan=3, pady=5)

        tk.Label(control_frame, text="Konfigurácia:").grid(row=22, column=0, sticky="w")
        self.save_dir = tk.StringVar(value="default")
        tk.Entry(control_frame, textvariable=self.save_dir, width=25).grid(row=22, column=1, columnspan=3, pady=5)

        tk.Button(control_frame, text="Draw", command=self.draw_figure).grid(row=23, column=0, columnspan=4, pady=5)
        tk.Button(control_frame, text="Nakresli šnúrku", command=self.draw_string_outline).grid(row=24, column=0, columnspan=4, pady=5)
        tk.Button(control_frame, text="Uložiť všetky emócie", command=self.save_all_emotions_images).grid(row=25, column=0, columnspan=4, pady=5)
        tk.Button(control_frame, text="Regeneruj všetky konfigurácie", command=self.regenerate_all_images_from_configs).grid(row=26, column=0, columnspan=4, pady=5)
        tk.Button(control_frame, text="Uložiť obrázok", command=self.save_canvas_as_jpg).grid(row=27, column=0, columnspan=4, pady=5)

        self.faces_dir = "position_generator/faces"
        bg_options = []

        if os.path.isdir(self.faces_dir):
            for fname in os.listdir(self.faces_dir):
                if fname.lower().endswith(".jpg"):
                    bg_options.append(fname)

        if not bg_options:
            bg_options = ["none"]

        default_bg = "normal.jpg" if "normal.jpg" in bg_options else bg_options[0]
        tk.Label(control_frame, text="Pozadie tváre:").grid(row=28, column=0, sticky="w")
        self.bg_image_var = tk.StringVar(value=default_bg)
        tk.OptionMenu(control_frame, self.bg_image_var, *bg_options).grid(row=28, column=1, columnspan=3, sticky="ew")
        self.bg_image = None
        self.bg_image_tk = None

        self.show_sticks_and_points = tk.BooleanVar(value=True)
        tk.Checkbutton(control_frame, text="Zobraziť ramená a body", variable=self.show_sticks_and_points, command=self.draw_figure).grid(row=29, column=0, columnspan=4, sticky="w")

        self.suspend_autoredraw = False

        for i in range(1, 7):
            self.points[i][0].trace_add("write", lambda *args: self.safe_draw())
            self.points[i][1].trace_add("write", lambda *args: self.safe_draw())
            self.left_lengths[i].trace_add("write", lambda *args: self.safe_draw())
            self.right_lengths[i].trace_add("write", lambda *args: self.safe_draw())
            self.angles[i].trace_add("write", lambda *args: self.safe_draw())

        self.safe_draw()

    def safe_draw(self):
        if getattr(self, 'suspend_autoredraw', False):
            return
        try:
            self.draw_figure()
        except tk.TclError:
            pass

    def draw_figure(self):
        self.canvas.delete("all")
        fname = self.bg_image_var.get()
        bg_image_path = os.path.join(self.faces_dir, fname)

        if os.path.exists(bg_image_path):
            img = Image.open(bg_image_path).resize((1000, 1000))
            self.bg_image_tk = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image_tk)

        self.draw_string_outline()

        if self.show_sticks_and_points.get():
            thickness = self.line_thickness.get() if self.line_thickness.get() != "" else 2

            for i in range(1, 7):
                x = self.points[i][0].get() if self.points[i][0].get() != "" else 0
                y = self.points[i][1].get() if self.points[i][1].get() != "" else 0
                left_len = self.left_lengths[i].get() if self.left_lengths[i].get() != "" else 0
                right_len = self.right_lengths[i].get() if self.right_lengths[i].get() != "" else 0
                angle = self.angles[i].get() if self.angles[i].get() != "" else 0

                left_x = x - left_len * cos(radians(angle))
                left_y = y - left_len * sin(radians(angle))
                right_x = x + right_len * cos(radians(angle))
                right_y = y + right_len * sin(radians(angle))

                self.canvas.create_line(x, y, left_x, left_y, fill="green", width=thickness)
                self.canvas.create_line(x, y, right_x, right_y, fill="green", width=thickness)
                self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")

    def save_config_txt(self, folder_path = None):
        if folder_path is None:
            folder_path = self.generated_images_dir
        config_path = os.path.join(folder_path, f"{self.save_dir.get()}_configuration.txt")
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(f"head_image={self.bg_image_var.get()}\n")
            for i in range(1, 7):
                x_val = self.points[i][0].get()
                y_val = self.points[i][1].get()
                left_len = self.left_lengths[i].get()
                right_len = self.right_lengths[i].get()
                f.write(f"Point {i}: x={x_val}, y={y_val}, left_length={left_len}, right_length={right_len}\n")

    def save_figure_to_file(self, file_path):
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = x + self.canvas.winfo_width()
        h = y + self.canvas.winfo_height()
        img = ImageGrab.grab(bbox=(x, y, w, h))
        img = img.convert("RGB")
        img.save(file_path, "JPEG")

    def save_canvas_as_jpg(self):
        if not self.save_dir.get():
            print("Prosím zadajte názov konfigurácie.")
            return
        try:
            self.save_config_txt()
            angles_str = '_'.join(str(self.angles[i].get()) for i in range(1, 7))
            save_path = os.path.join(self.generated_images_dir, f"{self.save_dir.get()}_angles_{angles_str}.jpg")
            self.save_figure_to_file(save_path)

            time.sleep(1) 
        except Exception as e:
            print(f"Obrázok sa nepodarilo uložiť: {e}")

    def save_all_emotions_images(self):
        if not self.save_dir.get():
            print("Prosím zadajte názov konfigurácie.")
            return
        
        try:
            self.save_config_txt()
            for emotion, (head_list, configs) in self.emotion_rotations.items():
                emotion_dir = os.path.join(self.generated_images_dir, emotion)
                os.makedirs(emotion_dir, exist_ok=True)

                for head in head_list:
                    self.bg_image_var.set(head)

                    for config in configs:

                        for i, angle in enumerate(config, start=1):
                            self.angles[i].set(angle)

                        self.root.update_idletasks()
                        self.draw_figure()
                        angles_str = '_'.join(str(a) for a in config)
                        filename = f"{self.save_dir.get()}_{head}_angles_{angles_str}.jpg"
                        save_path = os.path.join(emotion_dir, filename)
                        self.save_figure_to_file(save_path)

        except Exception as e:
            print(f"Obrázky sa nepodarilo uložiť: {e}")

    def regenerate_all_images_from_configs(self):
        for emotion in self.emotion_rotations.keys():
            emotion_dir = os.path.join(self.generated_images_dir, emotion)

            if os.path.isdir(emotion_dir):
                for fname in os.listdir(emotion_dir):
                    fpath = os.path.join(emotion_dir, fname)

                    try:
                        os.remove(fpath)
                    except Exception:
                        pass
                try:
                    os.rmdir(emotion_dir)
                except Exception:
                    pass

        config_dir = self.generated_images_dir
        config_names = [] 

        for fname in os.listdir(config_dir):
            if fname.endswith("_configuration.txt"):
                config_name = fname.replace("_configuration.txt", "")
                config_names.append(config_name)

        for config in config_names:
            config_path = os.path.join(config_dir, f"{config}_configuration.txt")

            if not os.path.exists(config_path):
                print(f"Konfiguračný súbor {config_path} neexistuje.")
                continue

            with open(config_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

                for i, line in enumerate(lines[1:], start=1):
                    parts = line.strip().split(", ")
                    x_val = int(parts[0].split("=")[1])
                    y_val = int(parts[1].split("=")[1])
                    left_len = int(parts[2].split("=")[1])
                    right_len = int(parts[3].split("=")[1])
                    self.points[i][0].set(x_val)
                    self.points[i][1].set(y_val)
                    self.left_lengths[i].set(left_len)
                    self.right_lengths[i].set(right_len)

            self.save_dir.set(config)
            self.root.update_idletasks()
            self.save_all_emotions_images()
            
    def draw_string_outline(self):
        circle_step = 5
        circle_radius = 10
        string_circle_color = "red"
        string_circle_width = 2
        string_circle_fill = "red"
        arm_circle_color = "red"
        arm_circle_width = 2
        arm_circle_fill = "red"
        curvatures = [0.85, 0.05, 0.8, 0.05]
        curvature_signs = [1, 1, -1, 1]
        curvature_scale_exponent = 0.8

        points = {}
        for i in range(1, 7):
            x = self.points[i][0].get()
            y = self.points[i][1].get()
            left_len = self.left_lengths[i].get()
            right_len = self.right_lengths[i].get()
            angle = self.angles[i].get()
            left_x = x - left_len * cos(radians(angle))
            left_y = y - left_len * sin(radians(angle))
            right_x = x + right_len * cos(radians(angle))
            right_y = y + right_len * sin(radians(angle))

            if i == 5:
                left_y += 15
            if i == 6:
                right_y += 15

            points[i] = {
                'center': (x, y),
                'left': (left_x, left_y),
                'right': (right_x, right_y)
            }

        def bezier_quad(p0, p1, p2, num=30):
            return [(
                (1-t)**2 * p0[0] + 2*(1-t)*t*p1[0] + t**2*p2[0],
                (1-t)**2 * p0[1] + 2*(1-t)*t*p1[1] + t**2*p2[1]
            ) for t in [i/num for i in range(num+1)]]

        pairs = [
            (points[1]['left'], points[3]['left']),
            (points[1]['right'], points[2]['left']),
            (points[2]['right'], points[4]['right']),
            (points[3]['right'], points[4]['left'])
        ]

        def get_control_point(p1, p2, curvature, sign):
            mx = (p1[0] + p2[0]) / 2
            my = (p1[1] + p2[1]) / 2
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            length = (dx**2 + dy**2) ** 0.5

            if length == 0:
                return (mx, my)
            
            perp_x = -dy / length
            perp_y = dx / length
            factor = curvature * (length ** curvature_scale_exponent)
            cx = mx + sign * perp_x * factor
            cy = my + sign * perp_y * factor

            return (cx, cy)

        full_path = []
        for idx, (p1, p2) in enumerate(pairs):
            control = get_control_point(p1, p2, curvature=curvatures[idx], sign=curvature_signs[idx])
            bezier_points = bezier_quad(p1, control, p2, num=30)

            if idx > 0:
                bezier_points = bezier_points[1:]

            full_path.extend(bezier_points)

        last_pos = None
        dist_accum = 0

        for i, pt in enumerate(full_path):
            if last_pos is None:
                self.canvas.create_oval(pt[0]-circle_radius, pt[1]-circle_radius, pt[0]+circle_radius, pt[1]+circle_radius, outline=string_circle_color, width=string_circle_width, fill=string_circle_fill)
                last_pos = pt
                continue

            dx = pt[0] - last_pos[0]
            dy = pt[1] - last_pos[1]
            dist = (dx**2 + dy**2) ** 0.5
            dist_accum += dist

            if dist_accum >= circle_step:
                self.canvas.create_oval(pt[0]-circle_radius, pt[1]-circle_radius, pt[0]+circle_radius, pt[1]+circle_radius, outline=string_circle_color, width=string_circle_width, fill=string_circle_fill)
                dist_accum = 0
                last_pos = pt

        for i in range(1, 5):
            for side in ['left', 'right']:
                p1 = points[i]['center']
                p2 = points[i][side]
                last_pos = None
                dist_accum = 0
                num_steps = 30

                for t in range(num_steps+1):
                    x = p1[0] + (p2[0] - p1[0]) * t / num_steps
                    y = p1[1] + (p2[1] - p1[1]) * t / num_steps
                    pt = (x, y)

                    if last_pos is None:
                        self.canvas.create_oval(x-circle_radius, y-circle_radius, x+circle_radius, y+circle_radius, outline=arm_circle_color, width=arm_circle_width, fill=arm_circle_fill)
                        last_pos = pt
                        continue

                    dx = pt[0] - last_pos[0]
                    dy = pt[1] - last_pos[1]
                    dist = (dx**2 + dy**2) ** 0.5
                    dist_accum += dist

                    if dist_accum >= circle_step:
                        self.canvas.create_oval(x-circle_radius, y-circle_radius, x+circle_radius, y+circle_radius, outline=arm_circle_color, width=arm_circle_width, fill=arm_circle_fill)
                        dist_accum = 0
                        last_pos = pt


        brows_circle_step = 3
        brows_circle_radius = 5
        brows_circle_color = "brown"
        brows_circle_width = 2
        brows_circle_fill = "brown"
        brows_curvature = 0.12
        brows_signs = [1, -1]

        for idx, i in enumerate(range(5, 7)):
            for side in ['left', 'right']:
                p1 = points[i]['center']
                p2 = points[i][side]

                if (i == 5 and side == 'left') or (i == 6 and side == 'right'):
                    dx = p2[0] - p1[0]
                    dy = p2[1] - p1[1]
                    length = (dx**2 + dy**2) ** 0.5
                    mx = (p1[0] + p2[0]) / 2
                    my = (p1[1] + p2[1]) / 2

                    if length == 0:
                        control = (mx, my)
                    else:
                        perp_x = -dy / length
                        perp_y = dx / length
                        factor = brows_curvature * length
                        sign = brows_signs[idx]
                        cx = mx + sign * perp_x * factor
                        cy = my + sign * perp_y * factor
                        control = (cx, cy)

                    num_steps = 30
                    bezier_points = bezier_quad(p1, control, p2, num=num_steps)
                    last_pos = None
                    dist_accum = 0

                    for pt in bezier_points:
                        x, y = pt
                        if last_pos is None:
                            self.canvas.create_oval(x-brows_circle_radius, y-brows_circle_radius, x+brows_circle_radius, y+brows_circle_radius, outline=brows_circle_color, width=brows_circle_width, fill=brows_circle_fill)
                            last_pos = pt
                            continue

                        dx = pt[0] - last_pos[0]
                        dy = pt[1] - last_pos[1]
                        dist = (dx**2 + dy**2) ** 0.5
                        dist_accum += dist

                        if dist_accum >= brows_circle_step:
                            self.canvas.create_oval(x-brows_circle_radius, y-brows_circle_radius, x+brows_circle_radius, y+brows_circle_radius, outline=brows_circle_color, width=brows_circle_width, fill=brows_circle_fill)
                            dist_accum = 0
                            last_pos = pt
                else:
                    last_pos = None
                    dist_accum = 0
                    num_steps = 30

                    for t in range(num_steps+1):
                        x = p1[0] + (p2[0] - p1[0]) * t / num_steps
                        y = p1[1] + (p2[1] - p1[1]) * t / num_steps
                        pt = (x, y)
                        
                        if last_pos is None:
                            self.canvas.create_oval(x-brows_circle_radius, y-brows_circle_radius, x+brows_circle_radius, y+brows_circle_radius, outline=brows_circle_color, width=brows_circle_width, fill=brows_circle_fill)
                            last_pos = pt
                            continue

                        dx = pt[0] - last_pos[0]
                        dy = pt[1] - last_pos[1]
                        dist = (dx**2 + dy**2) ** 0.5
                        dist_accum += dist
                        
                        if dist_accum >= brows_circle_step:
                            self.canvas.create_oval(x-brows_circle_radius, y-brows_circle_radius, x+brows_circle_radius, y+brows_circle_radius, outline=brows_circle_color, width=brows_circle_width, fill=brows_circle_fill)
                            dist_accum = 0
                            last_pos = pt


if __name__ == "__main__":
    root = tk.Tk()
    app = StickFigureApp(root, generated_images_dir="position_generator/generated_images_v3")
    root.mainloop()