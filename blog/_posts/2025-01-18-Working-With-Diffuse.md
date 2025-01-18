---
title: "Getting Started Working with Diffuse Scattering Data"
mathjax: false
layout: post
---

## Install `cctbx`
1. Install `miniconda3` [link](https://docs.anaconda.com/miniconda/install/)
2. Install `homebrew` [link](https://brew.sh/) 
3. Run: `conda create -n cctbx_env_2025 -c conda-forge cctbx-base`
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
min_indices = np.min(indices, axis=0)
min_indices = np.min(indices_np, axis=0)
max_indices = np.max(indices_np, axis=0)
shape = max_indices - min_indices + 1
volume = np.zeros(shape)
adjusted_indices = indices_np - min_indices
volume[tuple(adjusted_indices.T)] = data_np

plt.imshow(volume[:, :, shape[2]//2])
plt.show()
```
