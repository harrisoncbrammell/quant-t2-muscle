import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import napari
import numpy as np
from pymatreader import read_mat

def ask_inputs():
    root = tk.Tk()
    root.title('Open T2 Maps')
    root.resizable(False, False)

    pre_var  = tk.StringVar()
    post_var = tk.StringVar()
    map_var  = tk.StringVar(value='ggm')

    def browse(var):
        path = filedialog.askopenfilename(parent=root, filetypes=[('MAT files', '*.mat')])
        if path:
            var.set(path)

    for row, (label, var) in enumerate([('Pre scan:', pre_var), ('Post scan:', post_var)]):
        tk.Label(root, text=label).grid(row=row, column=0, sticky='w', padx=5, pady=4)
        tk.Entry(root, textvariable=var, width=55).grid(row=row, column=1, padx=5)
        tk.Button(root, text='Browse', command=lambda v=var: browse(v)).grid(row=row, column=2, padx=5)

    tk.Label(root, text='Map:').grid(row=2, column=0, sticky='w', padx=5, pady=4)
    tk.Entry(root, textvariable=map_var, width=20).grid(row=2, column=1, sticky='w', padx=5)

    result = {}
    def ok():
        if not pre_var.get() or not post_var.get():
            messagebox.showerror('Missing files', 'Please select both Pre and Post .mat files.')
            return
        result.update(pre=pre_var.get(), post=post_var.get(), map=map_var.get() or 'ggm')
        root.destroy()

    tk.Button(root, text='OK',     command=ok).grid(row=3, column=1, sticky='e', pady=8)
    tk.Button(root, text='Cancel', command=root.destroy).grid(row=3, column=2, pady=8)

    root.mainloop()
    return result

inputs = ask_inputs()
if not inputs:
    sys.exit(0)

map_name = inputs['map']
pre  = np.moveaxis(read_mat(inputs['pre'])[map_name],  -1, 0)
post = np.moveaxis(read_mat(inputs['post'])[map_name], -1, 0)

def add_label(viewer, img, name, text):
    n = img.shape[0]
    viewer.add_image(img, name=name, colormap='magma')
    viewer.add_points(
        [[s, 10, 10] for s in range(n)],
        features={'label': [text] * n},
        text={'string': '{label}', 'size': 20, 'color': 'white', 'anchor': 'upper_left'},
        size=0, face_color='transparent', out_of_slice_display=True, name=f'_{name}',
    )

viewer = napari.Viewer(title=f'{map_name.upper()}: Pre vs Post')
add_label(viewer, pre,  'Pre',  'PRE')
add_label(viewer, post, 'Post', 'POST')
viewer.grid.enabled = True
viewer.grid.stride = 2

napari.run()