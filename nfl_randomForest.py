# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 19:24:06 2019

@author: Walter King
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

##FIX STEVE SMITH (WR) MADDEN RATINGS

iteration = 1
year_iteration = 1

for year in range(2006, 2014):
    iteration = 1
    for position_group in ['WR','FS','CB','SS','ILB','RB','TE','EDGE','C','DT','OT','OG']:
        draftData = pd.read_csv(r'file_directory')
        train_data = draftData[:].query('position == "' + position_group + "\" and year != \"" + str(year) + "\"")
        test_data = draftData[:].query('position == "' + position_group + "\" and year == \"" + str(year) + "\"")
        exportfeatures = test_data.copy()
        labels_train = np.array(train_data['rating'])
        train_data = train_data.drop(['full_name','first_name','last_name','draft_team','college','position'
                                      ,'pos_distance','birth_date','class','year','round','pick','overall'
                                      ,'rating','ds_rank'], axis = 1)
        column_names = train_data.columns
        train_data = np.array(train_data)
        labels = np.array(test_data['rating'])
        test_data = test_data.drop(['full_name','first_name','last_name','draft_team','college','position'
                                    ,'pos_distance','birth_date','class','year','round','pick','overall'
                                    ,'rating','ds_rank'], axis = 1)
        test_data = np.array(test_data)
        train_features, test_features, train_labels, test_labels = \
        train_test_split(train_data, labels_train, test_size = 0.25, random_state = 42)
        rf = RandomForestRegressor(n_estimators = 1000, random_state = 42, max_depth = 15, max_features = 15, min_samples_leaf = 5)
        model = rf.fit(train_features, train_labels);
        predictions = model.predict(test_data)
        exportfeatures['prediction'] = predictions
        exportfeatures.to_csv('dumpfile.csv')
        if iteration == 1:
            predicted_data = pd.read_csv('dumpfile.csv')
        else:
            append_data = pd.read_csv('dumpfile.csv')
            predicted_data = predicted_data.append(pd.DataFrame(data = append_data), ignore_index=True)
        iteration += 1
        predicted_data.to_csv('dumpfile.csv')
    if year_iteration == 1:
        master_data = pd.read_csv('dumpfile.csv')
    else:
        year_append = pd.read_csv('dumpfile.csv')
        master_data = master_data.append(pd.DataFrame(data = year_append), ignore_index=True)
    year_iteration += 1
    master_data.to_csv('dumpfile.csv')


#feature_importances = pd.DataFrame(rf.feature_importances_,index = column_names,columns=['importance']).sort_values('importance',ascending=False)
#print(feature_importances)








