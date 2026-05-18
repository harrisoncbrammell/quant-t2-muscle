import napari
import numpy as np
from pymatreader import read_mat

data_pre = read_mat(r'C:\Users\harrison\Box\T2_data\Results\Pre_treatment\AD-20\se_mc_9slices_(Images)_39_MR\AD-20.se_mc_9slices_(Images)_39_MR.t2maps.mat')
data_post = read_mat(r'C:\Users\harrison\Box\T2_data\Results\Post_treatment\AD-20\se_mc_9slices_(Images)_81_MR\AD-20.se_mc_9slices_(Images)_81_MR.t2maps.mat')

ggm_pre = np.moveaxis(np.array(data_pre['ggm']), -1, 0)
ggm_post = np.moveaxis(np.array(data_post['ggm']), -1, 0)

viewer = napari.Viewer(title='GGM: Pre vs Post')
viewer.add_image(ggm_pre, name='Pre', colormap='magma')
viewer.add_image(ggm_post, name='Post', colormap='magma')
viewer.grid.enabled = True

h, w = ggm_pre.shape[-2], ggm_pre.shape[-1]
label_points = np.array([[0, 10, 10], [0, 10, 10]])
label_text = {'string': ['PRE', 'POST'], 'size': 18, 'color': 'white', 'anchor': 'upper_left'}
viewer.add_points(label_points, name='labels', text=label_text, size=0, face_color='transparent', features={'label': ['PRE', 'POST']})

napari.run()