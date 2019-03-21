# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 19:24:06 2019

@author: Walter King
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt
from statistics import mean


iteration = 1
year_iteration = 1

#randomizer_list = ['wt','yd40','yd20','yd10','bench','vert','broad','shut20','cone3']
#sigma_list =  [3*1, 0.038*1, 0.0325*1, 0.0285*1, 1.278*1, 1.171*1, 2.178*1, 0.0775*1, 0.1115*1]  

stat_list = ['adj_att','adj_ruyds','adj_rutd','adj_rec','adj_reyds','adj_retd','adj_scrim_yds','adj_off_td'\
             ,'adj_tkl','adj_ast_tkl','adj_tot_tkl','adj_run_stuff','adj_sk','adj_tfl','adj_int','adj_pass_def'\
             ,'adj_ff','adj_fr','disruption','ktd','ptd','int_td','fr_td','non_off_td','off_pass_cmp','off_pass_att'\
             ,'off_rush_att','def_pass_att','def_rush_att','team_sp','offense_sp','defense_sp','schedule_sp'\
             ,'off_usage','rel_usage','rel_disruption','weighted_def_sp']

depth_list = []
rms_list = []
prediction_log = []
importance_dict = {}
hyperparameters = {'WR':[100,10,10,14],
                   'FS':[50,5,10,3],
                   'CB':[50,10,20,2],
                   'SS':[250,15,10,3],
                   'ILB':[100,10,20,10],
                   'RB':[250,10,10,1],
                   'TE':[100,5,15,14],
                   'EDGE_LB':[100,15,5,2],
                   'EDGE_DL':[250,15,20,1],
                   'C':[20,5,10,3],
                   'DT':[20,5,10,10],
                   'OT':[250,15,20,1],
                   'OG':[250,5,20,18]}

# include adjacent position groups in dataset
# weight same position more heavily?
fuzzy_pos_groups = {'WR':['WR','RB','TE','CB'],
                    'FS':['FS','CB','SS','RB'],
                    'CB':['CB','FS','WR'],
                    'SS':['SS','FS','ILB'],
                    'ILB':['ILB','EDGE_LB','SS','WR'],
                    'RB':['RB','WR','ILB'],
                    'TE':['TE','WR','OT'],
                    'EDGE_LB':['EDGE_LB','EDGE_DL','ILB'],
                    'EDGE_DL':['EDGE_DL','DT','EDGE_LB','TE'],
                    'C':['OG','C'],
                    'DT':['EDGE_DL','DT','EDGE_LB','ILB'],
                    'OT':['OT','OG','C','EDGE_DL'],
                    'OG':['OT','OG','C']}


## training data
#for position_group in ['OG']:
#    draftData = pd.read_csv(r'C:\Users\Walter King\Documents\Combine Data\data_files\combined_draft_classes_randomForest.csv')
#    for s in stat_list:
#        try:
#            draftData[s].fillna(draftData.groupby(['position','pos_group'])[s].transform("median"), inplace=True)
#        except:
#            draftData[s].fillna(value = 0)   
#    draftData.fillna(value = 0)    
#    train_data = draftData[:].query('position == "' + position_group + "\"")
#    test_data = draftData[:].query('position == "' + position_group + "\"")
#    test_data = test_data.reset_index(drop=True)
#    exportfeatures = test_data.copy()
#    labels_train = np.array(train_data['rating'])
#    train_data = train_data.drop(['full_name','first_name','last_name','draft_team','college','position'
#                                  ,'pos_group','round','pick','overall','rating','year','consensus'], axis = 1)
#    column_names = train_data.columns
#    train_data = np.array(train_data)
#    labels = np.array(test_data['rating'])
#    test_data = test_data.drop(['full_name','first_name','last_name','draft_team','college','position'
#                                ,'pos_group','round','pick','overall','rating','year','consensus'], axis = 1)
#    test_data = np.array(test_data)
#    train_features, test_features, train_labels, test_labels = \
#    train_test_split(train_data, labels_train, test_size = 0.25, random_state = 42)
#    rf = RandomForestRegressor(n_estimators = hyperparameters[position_group][0], 
#                               random_state = 42, 
#                               max_depth = hyperparameters[position_group][1], 
#                               max_features = hyperparameters[position_group][2], 
#                               min_samples_leaf = hyperparameters[position_group][3])
#    train_features[np.isnan(train_features)] = 0
#    test_features[np.isnan(test_features)] = 0
#    train_data[np.isnan(train_data)] = 0
#    test_data[np.isnan(test_data)] = 0
#    model = rf.fit(train_features, train_labels);
#    feature_importances = pd.DataFrame(rf.feature_importances_,index = column_names,columns=['importance']).sort_values('importance',ascending=False)
#    #print(position_group)
#    #print(feature_importances)
#    prediction = model.predict(train_data)
#    exportfeatures['prediction'] = prediction
#    exportfeatures.to_csv('dumpfile.csv') 
#    # list of top 10 features
#    plot_features = feature_importances['importance'][0:10].index.tolist()
#    plot_importances = feature_importances['importance'][0:10].values.tolist()
#    y_pos = np.arange(len(plot_features))
#    plt.barh(y_pos, plot_importances, align='center', alpha=0.5)
#    plt.yticks(y_pos, plot_features)
#    plt.xlabel('Importance')
#    plt.title('Top 10 Features by Importance -- ' + position_group)
#    plt.show()


for m in [1]:
    random_iteration = 1
    for i in range(0,1):
    #for i in range(0, m):
        year_iteration = 1
        for year in range(2006, 2015):
            iteration = 1
            for position_group in ['CB','FS','SS','ILB','EDGE_DL','EDGE_LB','DT','WR','RB','TE','OT','OG','C']:
            #for position_group in ['WR']:
                fuzzy_group = fuzzy_pos_groups[position_group]
                draftData = pd.read_csv(r'C:\Users\Walter King\Documents\Combine Data\data_files\combined_draft_classes_randomForest.csv')
                for s in stat_list:
                    try:
                        draftData[s].fillna(draftData.groupby(['position','pos_group'])[s].transform("median"), inplace=True)
                    except:
                        draftData[s].fillna(value = 0)
                draftData.fillna(value = 0)
                # training data will now include adjacent position groups
                train_data = draftData[draftData['position'].isin(fuzzy_group)]
                train_data = train_data[:].query("year != \"" + str(year) + "\"")
                same_pos = train_data[:].query('position == "' + position_group + "\"")
                # ensure same position type is most prevalent in training set
                while train_data[train_data['position'] == position_group].count()['position'] <= \
                        train_data[train_data['position'] != position_group].count()['position']:
                    train_data = pd.concat([train_data, same_pos])
                #train_data = draftData[:].query('position == "' + position_group + "\" and year != \"" + str(year) + "\"")
                test_data = draftData[:].query('position == "' + position_group + "\" and year == \"" + str(year) + "\"")
                test_data = test_data.reset_index(drop=True)
                ## randomly shuffle data
#                for r in range(len(randomizer_list)):
#                    stat_name = randomizer_list[r]
#                    sigma = sigma_list[r]
#                    np.random.seed(random_iteration + year_iteration + iteration + i)
#                    randomized_list = np.random.normal(0, sigma, len(test_data[stat_name]))
#                    for i in range(len(test_data[stat_name])):
#                        test_data.loc[i, stat_name] += randomized_list[i]
#                ## re-calculate engineered features with randomized data
#                for i in range(len(test_data)):
#                    test_data.loc[i, 'bmi'] = (703 * test_data.loc[i, 'wt']) / (test_data.loc[i, 'ht'] ** 2)
#                    test_data.loc[i, 'speed_score'] = (200 * test_data.loc[i, 'wt']) / (test_data.loc[i, 'yd40'] ** 4)
#                    test_data.loc[i, 'ht_adj_speed_score'] = test_data.loc[i, 'speed_score'] * ((test_data.loc[i, 'ht'] / 73.5) ** 1.5)
#                    test_data.loc[i, 'vert_power'] = (60.7 * 2.54 * test_data.loc[i, 'vert']) + (45.3 * .4536 * test_data.loc[i, 'wt']) - 2055
#                    test_data.loc[i, 'broad_power'] = (60.7 * 2.54 * test_data.loc[i, 'broad']) + (45.3 * .4536 * test_data.loc[i, 'wt']) - 2055
#                    test_data.loc[i, 'quickness_score'] = (200 * test_data.loc[i, 'wt']) / (mean([test_data.loc[i, 'yd10'],test_data.loc[i, 'shut20'],test_data.loc[i, 'cone3']]) ** 4)
#                    test_data.loc[i, 'adj_bench'] = ((225 * test_data.loc[i, 'bench']) / test_data.loc[i, 'wt']) + test_data.loc[i, 'arm_length'] - 32.61
#                    test_data.loc[i, 'catch_radius'] = test_data.loc[i, 'ht'] + test_data.loc[i, 'vert'] + test_data.loc[i, 'arm_length'] + \
#                        mean([30 / (test_data.loc[i, 'yd40'] - test_data.loc[i, 'yd20']),30 / test_data.loc[i, 'shut20']]) * 12 + test_data.loc[i, 'broad'] + \
#                        (45 / test_data.loc[i, 'cone3']) * 12 + test_data.loc[i, 'wingspan']
                exportfeatures = test_data.copy()
                labels_train = np.array(train_data['rating'])
                train_data = train_data.drop(['full_name','first_name','last_name','draft_team','college','position'
                                              ,'pos_group','round','pick','overall','rating','year','consensus'], axis = 1)
                if position_group in ['CB','FS','SS','ILB','EDGE_LB','EDGE_DL','DT']:
                    train_data = train_data.drop(['adj_att','adj_ruyds','adj_rutd','adj_rec','adj_reyds','adj_retd','adj_scrim_yds'
                                                  ,'adj_off_td','off_pass_cmp','off_pass_att','off_rush_att','off_usage','rel_usage'], axis = 1)
                else:
                    train_data = train_data.drop(['adj_tkl','adj_ast_tkl','adj_tot_tkl','adj_run_stuff','adj_sk','adj_tfl'
                                                  ,'adj_int','adj_pass_def','adj_ff','adj_fr','int_td','fr_td','def_td'
                                                  ,'def_pass_att','def_rush_att','disruption','rel_disruption','weighted_def_sp'], axis = 1)
                column_names = train_data.columns
                train_data = np.array(train_data)
                labels = np.array(test_data['rating'])
                test_data = test_data.drop(['full_name','first_name','last_name','draft_team','college','position'
                                            ,'pos_group','round','pick','overall','rating','year','consensus'], axis = 1)
                if position_group in ['CB','FS','SS','ILB','EDGE_LB','EDGE_DL','DT']:
                    test_data = test_data.drop(['adj_att','adj_ruyds','adj_rutd','adj_rec','adj_reyds','adj_retd','adj_scrim_yds'
                                                  ,'adj_off_td','off_pass_cmp','off_pass_att','off_rush_att','off_usage','rel_usage'], axis = 1)
                else:
                    test_data = test_data.drop(['adj_tkl','adj_ast_tkl','adj_tot_tkl','adj_run_stuff','adj_sk','adj_tfl'
                                                  ,'adj_int','adj_pass_def','adj_ff','adj_fr','int_td','fr_td','def_td'
                                                  ,'def_pass_att','def_rush_att','disruption','rel_disruption','weighted_def_sp'], axis = 1)
                test_data = np.array(test_data)
                train_features, test_features, train_labels, test_labels = \
                train_test_split(train_data, labels_train, test_size = 0.25, random_state = 42)
                rf = RandomForestRegressor(n_estimators = hyperparameters[position_group][0], 
                                           random_state = 42, 
                                           max_depth = hyperparameters[position_group][1], 
                                           max_features = hyperparameters[position_group][2], 
                                           min_samples_leaf = hyperparameters[position_group][3])
                ## replace null values with 0
                train_features[np.isnan(train_features)] = 0
                test_features[np.isnan(test_features)] = 0
                train_data[np.isnan(train_data)] = 0
                test_data[np.isnan(test_data)] = 0
                model = rf.fit(train_features, train_labels);
                feature_importances = pd.DataFrame(rf.feature_importances_,index = column_names,columns=['importance']).sort_values('importance',ascending=False)
                #print(position_group)
                #print(feature_importances)
                prediction = model.predict(test_data)
                exportfeatures['prediction'] = prediction
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
                for n in range(len(feature_importances)):
                    importance_dict[feature_importances.iloc[n].name] = []
            else:
                year_append = pd.read_csv('dumpfile.csv')
                master_data = master_data.append(pd.DataFrame(data = year_append), ignore_index=True)
            for n in range(len(feature_importances)):
                importance_dict[feature_importances.iloc[n].name].append(feature_importances.iloc[n]['importance'])
            year_iteration += 1
            master_data.to_csv('dumpfile.csv')
            rating_list = master_data['rating'].tolist()
            prediction_list = master_data['prediction'].tolist()
            rms = sqrt(mean_squared_error(rating_list, prediction_list))
        depth_list.append(m)
        rms_list.append(rms)
#        print(m)
        prediction = master_data['prediction'].tolist()
        if random_iteration == 1:    
            prediction_log = [[i] for i in prediction]
        else:
            for i in range(len(prediction)):
                prediction_log[i].append(prediction[i])
        random_iteration += 1
    prediction_list = []
    for i in range(len(prediction_log)):
        pred_avg = sum(prediction_log[i]) / len(prediction_log[0])
        prediction_list.append(pred_avg)     
#    pull RMSE
    rating_list = master_data['rating'].tolist()
    prediction_list = master_data['prediction'].tolist()
    rms = sqrt(mean_squared_error(rating_list, prediction_list))
    print(rms)
    depth_list.append(m)
    rms_list.append(rms)


master_data['prediction'] = prediction_list
master_data.to_csv('dumpfile.csv') 


# hyperparameter tuning (rmse)
#from matplotlib.legend_handler import HandlerLine2D
#plt.plot(depth_list, rms_list, 'r', label='Validation RMSE')
#plt.ylabel('RMSE', fontsize = 10)
#plt.xlabel('Random Iterations', fontsize = 10)
#plt.title('Hyperparameter Tuning', fontsize = 14)
#plt.show()


## plotting feature importance
#plot_features = list(importance_dict.keys())
#plot_importances = []
#
#for f in plot_features:
#    plot_importances.append(mean(importance_dict[f]))
#
#plot_features_clean = []
#plot_importances_clean = []
#
#for i in range(len(plot_importances)):
#    if plot_importances[i] > 0:
#        plot_features_clean.append(plot_features[i])
#        plot_importances_clean.append(plot_importances[i])
#
#y_pos = np.arange(len(plot_features_clean))
#
#plt.barh(y_pos, plot_importances_clean, align='center', alpha=0.5)
#plt.yticks(y_pos, plot_features_clean)
#plt.xlabel('Importance')
#plt.title('Features Importances')
#plt.show()





















