#!/home/jim/anaconda2/envs/py35/bin/python
"""
Code for making predictions on new data   
_Author: Jimmy Charité_  
_Email: jimmy.charite@gmail.com_  
_Date: January 9, 2017_
"""

# Packages
###############################################################################
import sys
import numpy as np
import pandas as pd
from sklearn.feature_selection import VarianceThreshold
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Arguments
###############################################################################
path_old_data = sys.argv[1] #full path of the old (training) data
path_colnames = sys.argv[2] #full path of colname file provided within the repo
path_new_data = sys.argv[3] #full path of the new data
path_pred_file = sys.argv[4] #full path of the prediction output data

# Data Prep Function
###############################################################################
def clean_data(data_path, col_name_path):
    #Upload the data
    raw_data=pd.read_csv(data_path,header=None)
    
    #Upload and edit the column names
    col_names=pd.read_csv(col_name_path,header=None,
                     sep=":")
    col_names.columns=['variable','type']
    col_names=pd.concat((col_names,
                     pd.DataFrame({'variable':['image_type'],
                                   'type':['0,1.'] })),axis=0)
    col_names=col_names[['variable','type']]

    #Add column namaes to the raw data
    raw_data.columns=list(col_names.variable)
    
    #Make the data numerical
    raw_data.replace({'image_type': {'nonad.':0,'ad.':1}},inplace=True)
    raw_data=raw_data.apply(lambda row: pd.to_numeric(row,errors='coerce'))
    raw_data.ix[raw_data.local.isnull(), 'local']=0

    #Make the Continuous variables Categorical
    raw_data['aratio_cat']='aratio_NaN'
    raw_data.ix[(raw_data.aratio>=0) & (raw_data.aratio<2), 
                'aratio_cat']='aratio_0t2'
    raw_data.ix[(raw_data.aratio>=2) & (raw_data.aratio<4), 
                'aratio_cat']='aratio_2t4'
    raw_data.ix[(raw_data.aratio>=4) & (raw_data.aratio<6), 
                'aratio_cat']='aratio_4t6'
    raw_data.ix[(raw_data.aratio>=6) & (raw_data.aratio<8), 
                'aratio_cat']='aratio_6t8'
    raw_data.ix[(raw_data.aratio>=8) & (raw_data.aratio<10), 
                'aratio_cat']='aratio_8t10'
    raw_data.ix[(raw_data.aratio>=10), 'aratio_cat']='aratio_10t'
    aspect_cats=pd.get_dummies(raw_data['aratio_cat'])
    del aspect_cats['aratio_NaN'] #comparison category
    del raw_data['aratio_cat']

    raw_data['height_cat']='height_NaN'
    raw_data.ix[(raw_data.height>=0) & (raw_data.height<50), 
                'height_cat']='height_0t50'
    raw_data.ix[(raw_data.height>=50) & (raw_data.height<100), 
                'height_cat']='height_50t100'
    raw_data.ix[(raw_data.height>=100) & (raw_data.height<150), 
                'height_cat']='height_100t150'
    raw_data.ix[(raw_data.height>=150) & (raw_data.height<200), 
                'height_cat']='height_150t200'
    raw_data.ix[(raw_data.height>=200) & (raw_data.height<250), 
                'height_cat']='height_200t250'
    raw_data.ix[(raw_data.height>=250) & (raw_data.height<300), 
                'height_cat']='height_250t300'
    raw_data.ix[(raw_data.height>=300) & (raw_data.height<350), 
                'height_cat']='height_300t350'
    raw_data.ix[(raw_data.height>=350) & (raw_data.height<400), 
                'height_cat']='height_350t400'
    raw_data.ix[(raw_data.height>=400), 'height_cat']='height_400t'
    height_cats=pd.get_dummies(raw_data['height_cat'])
    del height_cats['height_NaN'] #comparison category
    del raw_data['height_cat']

    raw_data['width_cat']='width_NaN'
    raw_data.ix[(raw_data.width>=0) & (raw_data.width<50), 
                'width_cat']='width_0t50'
    raw_data.ix[(raw_data.width>=50) & (raw_data.width<100), 
                'width_cat']='width_50t100'
    raw_data.ix[(raw_data.width>=100) & (raw_data.width<150), 
                'width_cat']='width_100t150'
    raw_data.ix[(raw_data.width>=150) & (raw_data.width<200), 
                'width_cat']='width_150t200'
    raw_data.ix[(raw_data.width>=200) & (raw_data.width<250), 
                'width_cat']='width_200t250'
    raw_data.ix[(raw_data.width>=250) & (raw_data.width<300), 
                'width_cat']='width_250t300'
    raw_data.ix[(raw_data.width>=300) & (raw_data.width<350), 
                'width_cat']='width_300t350'
    raw_data.ix[(raw_data.width>=350) & (raw_data.width<400), 
                'width_cat']='width_350t400'
    raw_data.ix[(raw_data.width>=400), 'width_cat']='width_400t'
    width_cats=pd.get_dummies(raw_data['width_cat'])
    del width_cats['width_NaN'] #comparison category
    del raw_data['width_cat']

    del raw_data['height'], raw_data['width'], raw_data['aratio']
    raw_data=pd.concat([height_cats,width_cats,aspect_cats,raw_data], axis=1)

    X = (raw_data.iloc[:,:-1]).as_matrix()
    y = (raw_data.iloc[:,-1]).tolist()
    
    return X, y
    
# Creating Sklearn Friendly Datasets
###############################################################################
X_train, y_train = clean_data(path_old_data, path_colnames)

X_test, y_test = clean_data(path_new_data, path_colnames)

# Model fitting and predictions
###############################################################################
vt=VarianceThreshold(threshold=0)
log_clf=LogisticRegression(C=10,class_weight={1: 1})
log_clf_est = Pipeline(steps=[('vt',vt),('clf',log_clf)])

log_clf_est.fit(X_train,y_train)

y_pred = log_clf_est.predict(X_test)

np.savetxt(path_pred_file, y_pred, delimiter=',')
