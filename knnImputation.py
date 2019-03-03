# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 08:20:03 2019

@author: Walter King
"""

## Props to Georgios Dakos for writing this helpful 2 part tutorial
## https://towardsdatascience.com/handling-missing-values-in-machine-learning-part-1-dda69d4f88ca
## https://towardsdatascience.com/handling-missing-values-in-machine-learning-part-2-222154b4b58e


import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
from fancyimpute import KNN
#from scipy.spatial import distance

## Load file
draft_data = pd.read_csv(r"file_directory.csv")


## Fill missing values in Age feature with each class’s median value ## of Age 
draft_data['draft_age'].fillna(draft_data.groupby('class')['draft_age'].transform("median"), inplace=True)

## Pearson Correlation Matrix plot
#colormap = plt.cm.RdBu
#plt.figure(figsize=(32,10))
#plt.title('Pearson Correlation of Features', y=1.05, size=15)
#sns.heatmap(draft_data.corr(),linewidths=0.1,vmax=1.0, 
#            square=True, cmap=colormap, linecolor='white', annot=True)


#fancy impute removes column names.
#draft_data_cols = list(draft_data)
draft_data_float = draft_data.select_dtypes(include=[np.float])
# Use k nearest rows which have a feature to fill in each row's
# missing features
draft_data = pd.DataFrame(KNN(k=7).fit_transform(draft_data_float))
#draft_data.columns = draft_data_cols

draft_data.to_csv('dumpfile.csv')


#distance.cityblock([ht_pos1, bmi_pos1, yd40_pos1], [ht_pos2, bmi_pos2, yd40_pos2])









