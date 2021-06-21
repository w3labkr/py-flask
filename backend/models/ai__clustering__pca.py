# Miscellaneous operating system interfaces
import os

# JSON encoder and decoder
import json

# Time access and conversions
import time

# A light weight extension of the default python dict object. This allows for the use of key names as object attributes.
from dotted_dict import DottedDict

# File Uploads
# https://flask.palletsprojects.com/en/1.1.x/quickstart/
from werkzeug.utils import secure_filename

# The fundamental package for scientific computing with Python.
import numpy as np

# Flexible and powerful data analysis / manipulation library for Python, providing labeled data structures similar to R data.frame objects, statistical functions, and much more
import pandas as pd

# Machine learning in Python
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Plotting with Python.
import matplotlib as mpl
import matplotlib.pyplot as plt

# If you are running a webserver and using it to save Matplotlib make sure to set the backend to a non-interactive one (matplotlib.use('agg') or matplotlib.pyplot.switch_backend('Agg')) so that your server does not try to create (and then destroy) GUI windows that will never be seen (or if they are will be more of a nuisance).
# mpl.use('agg')
mpl.pyplot.switch_backend('Agg')

# The Python micro framework for building web applications.
from flask import session

# Import the application's modules and packages.
from modules.os import get_app_dir, get_latest_file, is_file, is_extensions

# Set the absolute directory path.
appdir = get_app_dir()


def constructor(request):
    obj = DottedDict({'iserror': False, 'errmsg': '', 'dataset': {}})
    form, files = DottedDict(request.form), request.files
    file = files[str(list(files)[0])]

    # Set up a validator.
    if 'username' not in session:
        obj.update({'iserror': True, 'errmsg': 'Username is not defined.'})
        return obj
    elif not form:
        obj.update({'iserror': True, 'errmsg': 'Form data is empty.'})
        return obj
    elif not is_file(file):
        obj.update({'iserror': True, 'errmsg': 'The file has not been uploaded.'})
        return obj
    elif not is_extensions(file, extensions=['csv', 'tsv']):
        obj.update({'iserror': True, 'errmsg': 'This file is not allowed.'})
        return obj

    # Set the default directory.
    if session.get('username') == 'anonymous':
        basedir = os.path.join(appdir.anonymous, session.get('uuid'))
    else:
        basedir = os.path.join(appdir.storage, session.get('username'))
    uploads_dir = os.path.join(basedir, 'uploads')

    # Save the file in the upload directory.
    filepath = os.path.join(uploads_dir, secure_filename(file.filename))
    file.save(filepath)

    # initial
    df = pd.DataFrame(columns=['A', 'B'], index=np.arange(1))

    try:
        raw = pd.read_csv(filepath)

        # Preprocessing
        # StandardScaler: Standardize features by removing the mean and scaling to unit variance
        scaler = StandardScaler()
        scaled = scaler.fit_transform(raw.drop('target', axis=1))

        # Decomposition
        # PCA: Principal Component Analysis
        data = PCA(n_components=2).fit_transform(scaled)
        df = pd.DataFrame(data, columns=['pca_x', 'pca_y'])
        df['target'] = raw['target']

        # K-Means Clustering
        n_clusters = int(form.get('kmeans__n_clusters'))
        model = KMeans(n_clusters=n_clusters, init='k-means++',
                       max_iter=300, random_state=2021)
        model.fit(data)
        df['cluster'] = model.labels_

        # Export DataFrame
        #obj['dataset']['dataframe'] = df
        #obj['dataset']['data'] = df.to_json()

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

        # Export Original Data
        basename = 'pca-origin-{}.png'.format(time.strftime("%Y%m%d%H%M%S"))
        basepath = os.path.join(basedir, basename)

        obj['dataset']['origin'] = {}
        obj['dataset']['origin']['image'] = basename

        plt.savefig(basepath, format='png', dpi=200)

    except Exception as e:
        obj.update({'iserror': True, 'errmsg': e})

    return obj
