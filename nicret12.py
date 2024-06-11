from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import askcolor
import tkinter as tk

class PaintApp:

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self, root):
        self.root = root
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white", bd=3, relief=SUNKEN)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.setup_navbar()
        self.setup_tools()
        self.setup_events()

        self.old_x = None
        self.old_y = None
        self.line_width = self.DEFAULT_PEN_SIZE
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = None

        self.prev_x = None
        self.prev_y = None

    def setup_navbar(self):
        self.navbar = Menu(self.root)
        self.root.config(menu=self.navbar)

        # File menu
        self.file_menu = Menu(self.navbar, tearoff=False)
        self.navbar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save Snapshot", command=self.take_snapshot)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit menu
        self.edit_menu = Menu(self.navbar, tearoff=False)
        self.navbar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.undo)

    def setup_tools(self):
        self.selected_tool = "pen"
        self.colors = ["black", "red", "green", "blue", "yellow", "orange", "purple"]
        self.selected_color = self.colors[0]
        self.brush_sizes = [2, 4, 6, 8, 10]
        self.selected_size = self.brush_sizes[0]
        self.pen_types = ["line", "round", "square", "arrow", "diamond"]
        self.selected_pen_type = self.pen_types[0]

        self.tool_frame = ttk.LabelFrame(self.root, text="Tools")
        self.tool_frame.pack(side=RIGHT, padx=5, pady=5, fill=Y)

        self.pen_button = ttk.Button(self.tool_frame, text="Pen", command=self.use_pen)
        self.pen_button.pack(side=TOP, padx=5, pady=5)

        self.eraser_button = ttk.Button(self.tool_frame, text="Eraser", command=self.use_eraser)
        self.eraser_button.pack(side=TOP, padx=5, pady=5)

        self.color_button = ttk.Button(self.tool_frame, text="Color", command=self.choose_color)
        self.color_button.pack(side=TOP, padx=5, pady=5)

        self.brush_size_label = ttk.Label(self.tool_frame, text="Brush Size:")
        self.brush_size_label.pack(side=TOP, padx=5, pady=5)

        self.brush_size_combobox = ttk.Combobox(self.tool_frame, values=self.brush_sizes, state="readonly")
        self.brush_size_combobox.current(0)
        self.brush_size_combobox.pack(side=TOP, padx=5, pady=5)
        self.brush_size_combobox.bind("<<ComboboxSelected>>", lambda event: self.select_size(int(self.brush_size_combobox.get())))

        self.color_label = ttk.Label(self.tool_frame, text="Color:")
        self.color_label.pack(side=TOP, padx=5, pady=5)

        self.color_combobox = ttk.Combobox(self.tool_frame, values=self.colors, state="readonly")
        self.color_combobox.current(0)
        self.color_combobox.pack(side=TOP, padx=5, pady=5)
        self.color_combobox.bind("<<ComboboxSelected>>", lambda event: self.select_color(self.color_combobox.get()))

        self.pen_type_label = ttk.Label(self.tool_frame, text="Pen Type:")
        self.pen_type_label.pack(side=TOP, padx=5, pady=5)

        self.pen_type_combobox = ttk.Combobox(self.tool_frame, values=self.pen_types, state="readonly")
        self.pen_type_combobox.current(0)
        self.pen_type_combobox.pack(side=TOP, padx=5, pady=5)
        self.pen_type_combobox.bind("<<ComboboxSelected>>", lambda event: self.select_pen_type(self.pen_type_combobox.get()))

        self.clear_button = ttk.Button(self.tool_frame, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.pack(side=TOP, padx=5, pady=5)

    def setup_events(self):
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def use_pen(self):
        self.selected_tool = "pen"
        self.activate_button(self.pen_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.selected_tool = "eraser"
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        if self.active_button:
            self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.brush_size_combobox.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            if self.selected_tool == "pen" and self.selected_pen_type == "line":
                self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=self.line_width, fill=paint_color, capstyle=ROUND, smooth=TRUE, splinesteps=36)
            elif self.selected_tool == "pen" and self.selected_pen_type == "round":
                x1 = event.x - int(self.line_width)
                y1 = event.y - int(self.line_width)
                x2 = event.x + int(self.line_width)
                y2 = event.y + int(self.line_width)
                self.canvas.create_oval(x1, y1, x2, y2, fill=paint_color, outline=paint_color)
            elif self.selected_tool == "pen" and self.selected_pen_type == "square":
                x1 = event.x - int(self.line_width)
                y1 = event.y - int(self.line_width)
                x2 = event.x + int(self.line_width)
                y2 = event.y + int(self.line_width)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=paint_color, outline=paint_color)
            elif self.selected_tool == "pen" and self.selected_pen_type == "arrow":
                x1 = event.x - int(self.line_width)
                y1 = event.y - int(self.line_width)
                x2 = event.x + int(self.line_width)
                y2 = event.y + int(self.line_width)
                self.canvas.create_polygon(x1, y1, x1, y2, event.x, y2, fill=paint_color, outline=paint_color)
            elif self.selected_tool == "pen" and self.selected_pen_type == "diamond":
                x1 = event.x - int(self.line_width)
                y1 = event.y
                x2 = event.x
                y2 = event.y - int(self.line_width)
                x3 = event.x + int(self.line_width)
                y3 = event.y
                x4 = event.x
                y4 = event.y + int(self.line_width)
                self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, fill=paint_color, outline=paint_color)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def select_size(self, size):
        self.selected_size = size

    def select_color(self, color):
        self.selected_color = color

    def select_pen_type(self, pen_type):
        self.selected_pen_type = pen_type

    def clear_canvas(self):
        self.canvas.delete("all")

    def take_snapshot(self):
        self.canvas.postscript(file="snapshot.eps")

    def undo(self):
        items = self.canvas.find_all()
        if items:
            self.canvas.delete(items[-1])

if __name__ == "__main__":
    root = Tk()
    root.title("Paint Application")
    app = PaintApp(root)
    root.mainloop()
