# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 19:48:13 2022

@author: sonaw
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('eda_data.csv')

#choose relevant columns
df.columns

df_model = df[['avg_salary','Rating','Size','Type of ownership','Industry','Sector','Revenue','num_comp','hourly','employer_provided',
             'job_state','same_state','age','python_yn','spark','aws','excel','job_simp','seniority','desc_len']]

# get dummies
df_dum = pd.get_dummies(df_model)

# train test split
from sklearn.model_selection import train_test_split

X = df_dum.drop('avg_salary', axis =1)
y = df_dum['avg_salary'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize numerical columns
from sklearn.preprocessing import MinMaxScaler
columns = ['Rating','age','num_comp']
scalar = MinMaxScaler()
scaled_features_train = scalar.fit_transform(X_train[columns].values)
scaled_features_test = scalar.transform(X_test[columns].values)
X_train[columns] = scaled_features_train
X_test[columns] = scaled_features_test

# multiple linear regression--> base model
from sklearn.linear_model import LinearRegression,Lasso
from sklearn.model_selection import cross_val_score

lm = LinearRegression()
lm.fit(X_train, y_train)

np.mean(cross_val_score(lm,X_train,y_train,scoring = 'neg_mean_absolute_error',cv=3))   
# -20.6983558688033


# lasso regression
lm_l = Lasso()
lm_l.fit(X_train,y_train)
np.mean(cross_val_score(lm_l,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3))
# -20.986837261817005

# hyper tuning lasso
alpha =[]
error = []

for i in range(1,1000):
    alpha.append(i/1000)
    lml = Lasso(alpha=(i/1000))
    error.append(np.mean(cross_val_score(lml,X_train,y_train,scoring = 'neg_mean_absolute_error',cv=3)))

plt.plot(alpha,error)

err = tuple(zip(alpha,error))
df_err = pd.DataFrame(err,columns=['alpha','error'])
df_err[df_err.error==max(df_err.error)]
# 0.099 -19.285512

# calculating score using best param
lm_l = Lasso(alpha=0.099)
lm_l.fit(X_train,y_train)
np.mean(cross_val_score(lm_l,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3))
# -19.285511828056798

# random forest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()
np.mean(cross_val_score(rf,X_train,y_train,scoring = 'neg_mean_absolute_error',cv=3))
# -14.999285195440015

# hyper parameter tuning using gridsearchcv
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,300,10),'criterion':('mse','mae'),'max_features':('auto', 'sqrt', 'log2')}

gs = GridSearchCV(rf, parameters,scoring = 'neg_mean_absolute_error', cv= 3)
gs.fit(X_train,y_train)

gs.best_score_    #-14.786760622685867
gs.best_estimator_

# evaluate against test data
pred_lm = lm.predict(X_test)
pred_lml = lm_l.predict(X_test)
pred_rf = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test,pred_lm)   # 18.817508457018814
mean_absolute_error(y_test,pred_lml)  # 19.570460706469262
mean_absolute_error(y_test,pred_rf)   # 11.055597925564369

import pickle
pickl = {'model':gs.best_estimator_}
pickle.dump(pickl,open('model_file.p','wb'))

file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']
    
model.predict(X_test.iloc[1,:].values.reshape(1,-1))

y_test[1]

list(X_test.iloc[1,:])