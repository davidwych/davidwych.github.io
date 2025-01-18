---
title: "Getting Started Working with Diffuse Scattering Data"
mathjax: false
layout: post
---

The following is instructions for the bare minimum in working with diffuse scattering data: viewing an `.mtz` file of diffuse scattering.

We'll create a `conda` environment, then create a python `.py` file for viewing the `.mtz` file, and then run it

<!--more-->

---

## Install `cctbx`
1. Install `miniconda3` [link](https://docs.anaconda.com/miniconda/install/)
2. Run: `conda create -n cctbx_env_2025 -c conda-forge cctbx-base`
3. Run: `conda activate cctbx_env_2025`
4. Run: `conda install cctbx`

Create a file called `view_slice.py` and paste the following code inside (you may need to change the label `F,SIGF` of your miller array to get your data):

```python
from iotbx import reflection_file_reader
from sys import argv
import numpy as np
import matplotlib.pyplot as plt

mtz_filename = argv[1]

mtz_file = reflection_file_reader.any_reflection_file(mtz_filename)
miller_arrays = mtz_file.as_miller_arrays()

data_array = None
for array in miller_arrays:
    if array.info().label_string() == 'F,SIGF':
        data_array = array
        break

data_np = np.array(data_array.data())
indices_np = np.array(data_array.indices())
min_indices = np.min(indices_np, axis=0)
max_indices = np.max(indices_np, axis=0)
shape = max_indices - min_indices + 1
volume = np.zeros(shape)
adjusted_indices = indices_np - min_indices
volume[tuple(adjusted_indices.T)] = data_np

class IndexTracker:
    def __init__(self, ax, X):
        self.ax = ax
        self.X = X
        self.slices = X.shape[0]
        self.ind = self.slices // 2

        self.im = ax.imshow(self.X[self.ind, :, :], cmap='viridis')
        self.update()

    def onscroll(self, event):
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        self.im.set_data(self.X[self.ind, :, :])
        self.ax.set_title(f'Slice {self.ind}')
        self.im.axes.figure.canvas.draw()

fig, ax = plt.subplots(1, 1)
tracker = IndexTracker(ax, volume)
fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
plt.show()
```

Then run: `python view_slice.py [YOUR MTZ FILE].mtz`

You should be able to scroll and view the slices through your `.mtz` file!
