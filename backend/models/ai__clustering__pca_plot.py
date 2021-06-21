# Miscellaneous operating system interfaces
import os

# The fundamental package for scientific computing with Python.
import numpy as np

# Flexible and powerful data analysis / manipulation library for Python, providing labeled data structures similar to R data.frame objects, statistical functions, and much more
import pandas as pd

# Machine learning in Python
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Core tools for working with streams
from io import BytesIO, StringIO

import base64

from PIL import Image

# Plotting with Python.
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG

# If you are running a webserver and using it to save Matplotlib make sure to set the backend to a non-interactive one (matplotlib.use('agg') or matplotlib.pyplot.switch_backend('Agg')) so that your server does not try to create (and then destroy) GUI windows that will never be seen (or if they are will be more of a nuisance).
# mpl.use('agg')
mpl.pyplot.switch_backend('Agg')

# Import the application's modules and packages.
from modules.os import get_app_dir

# Set the absolute directory path.
appdir = get_app_dir()


def constructor(df):

    obj = {'iserror': False, 'errmsg': '', 'dataset': {}}

    # ValueError: The truth value of a dataframe is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
    # if (not df):
    #     return obj

    try:
        # Plots
        markers = ['s', 'o', '^', 'P', 'D', 'H', 'x', ',', '+', '.', 'o', '*']

        # Original Data
        fig = plt.figure()
        for v in df.target.unique():
            x_axis = df.query("target == @v")['pca_x']
            y_axis = df.query("target == @v")['pca_y']
            plt.scatter(x_axis, y_axis, marker=markers[v])

        plt.title('Original Data Visualization by 2 PCA Components')
        plt.xlabel('PCA X')
        plt.ylabel('PCA Y')

        # how to save a pylab figure into in-memory file which can be read into PIL image?
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=200)
        buf.seek(0)
        img = Image.open(buf)
        return img
        
        # Cluster Data
        # plt.figure()
        # try:
        #     for i in np.arange(n_clusters):    
        #         x_axis = df.query("cluster == @i")['pca_x']
        #         y_axis = df.query("cluster == @i")['pca_y']
                
        #         plt.scatter(x_axis, y_axis, marker=markers[i])
        # except Exception as e:
        #     obj.update({'iserror': True, 'errmsg': e})

        # plt.title('{} Clusters Visualization by 2 PCA Components'.format(n_clusters))
        # plt.xlabel('PCA X')
        # plt.ylabel('PCA Y')

        # img = BytesIO()
        # plt.savefig(img, format='png', dpi=200)
        # img.seek(0)

        # obj['dataset']['images'].append(img)

    except Exception as e:
        obj.update({'iserror': True, 'errmsg': e})

    return obj
