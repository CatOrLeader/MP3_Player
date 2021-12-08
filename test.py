import tkinter as tk
import tkinter as tk
from tkinter import ttk
from ttkwidgets import TickScale

def set_img_color(img, color):
    """Change color of PhotoImage img."""
    pixel_line = "{" + " ".join(color for i in range(img.width())) + "}"
    pixels = " ".join(pixel_line for i in range(img.height()))
    img.put(pixels)

root = tk.Tk()
# create images used for the theme
slider_width = 30
slider_height = 15
# normal slider
img_slider = tk.PhotoImage('img_slider', width=slider_width, height=slider_height, master=root)
set_img_color(img_slider, "red")
# active slider
img_slider_active = tk.PhotoImage('img_slider_active', width=slider_width, height=slider_height, master=root)
set_img_color(img_slider_active, '#1065BF')

style = ttk.Style(root)
style.theme_use('clam')
# create scale element
style.element_create('custom.Horizontal.Scale.slider', 'image', img_slider,
                     ('active', img_slider_active))
# create custom layout
style.layout('custom.Horizontal.TScale',
             [('Horizontal.Scale.trough',
               {'sticky': 'nswe',
                'children': [('custom.Horizontal.Scale.slider',
                              {'side': 'left', 'sticky': ''})]})])
style.configure('custom.Horizontal.TScale', background='black', foreground='grey',
                troughcolor='#73B5FA')
scale = TickScale(root, from_=0, to=100, tickinterval=100, orient="horizontal",
                  style='custom.Horizontal.TScale')
scale.pack(fill='x')
root.mainloop()