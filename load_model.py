import pickle
import gzip
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
import sys
import joblib

# with open('Dest_map.pkl','wb') as tf:
#     Dest_map = pickle.load(tf)
# with open('Origin_map.pkl') as tf:
#     Origin_map = pickle.load(tf)


def predict_ans(file_name):
    data_pred = pd.DataFrame(file_name)
    data_pred = data_pred.T
    
    columns = ['Year', 'Quarter', 'Month', 'DayofMonth', 'DayOfWeek',
           'IATA_Code_Marketing_Airline', 'Origin', 'Dest', 'CRSDepTime',
           'CRSArrTime', 'DistanceGroup',
           
           'AWND_x', 'PRCP_x', 'TMAX_x', 'TMIN_x', 'WSF2_x',
           'WSF5_x', 'SNOW_x', 'WT01_x', 'WT02_x', 'WT03_x', 'WT04_x', 'WT05_x',
           'WT06_x', 'WT07_x', 'WT08_x', 'WT09_x', 'WT10_x', 'WT11_x', 'WT18_x',
           
           'AWND_y', 'PRCP_y', 'TMAX_y', 'TMIN_y', 'WSF2_y', 
           'WSF5_y', 'SNOW_y', 'WT01_y', 'WT02_y', 'WT03_y', 'WT04_y', 'WT05_y', 
           'WT06_y', 'WT07_y', 'WT08_y', 'WT09_y', 'WT10_y', 'WT11_y', 'WT18_y',
           ]
    
    col_dict = {}
    for i in range(len(columns)):
        col_dict[i]=columns[i]
        
    data_pred.rename(columns=col_dict,inplace=True)
    print(data_pred)

    data_pred.reset_index(drop=True,inplace=True)
 
    data_pred['WTSUMx'] = (data_pred['WT01_x']+data_pred['WT02_x']+data_pred['WT03_x']+data_pred['WT04_x']+
                           data_pred['WT05_x']+data_pred['WT06_x']+data_pred['WT07_x']+data_pred['WT08_x']+
                           data_pred['WT09_x']+data_pred['WT10_x']+data_pred['WT11_x']+data_pred['WT18_x'])
    
    data_pred['WTSUMy'] = (data_pred['WT01_y']+data_pred['WT02_y']+data_pred['WT03_y']+data_pred['WT04_y']+
                           data_pred['WT05_y']+data_pred['WT06_y']+data_pred['WT07_y']+data_pred['WT08_y']+
                           data_pred['WT09_y']+data_pred['WT10_y']+data_pred['WT11_y']+data_pred['WT18_y'])
    
    
    
    data_copy = data_pred.copy()
    
    data_copy['IATA_Code_Marketing_Airline'] = LabelEncoder().fit_transform(data_copy['IATA_Code_Marketing_Airline'])


    # data_copy['Dest'] = data_copy['Dest'].map(Dest_map)

    # data_copy['Origin'] = data_copy['Origin'].map(Origin_map)
    
    col_select =['Year', 'Quarter', 'Month', 'DayofMonth', 'DayOfWeek',
           'IATA_Code_Marketing_Airline', 'Origin', 'Dest', 'CRSDepTime',
           'CRSArrTime', 'DistanceGroup',
           
           'AWND_x', 'PRCP_x', 'TMAX_x', 'TMIN_x', 'WSF2_x',
           'WSF5_x', 'SNOW_x', 'WT01_x', 'WT02_x', 'WT03_x', 'WT04_x', 'WT05_x',
           'WT06_x', 'WT07_x', 'WT08_x', 'WT09_x', 'WT10_x', 'WT11_x', 'WT18_x',
           
           'AWND_y', 'PRCP_y', 'TMAX_y', 'TMIN_y', 'WSF2_y', 
           'WSF5_y', 'SNOW_y', 'WT01_y', 'WT02_y', 'WT03_y', 'WT04_y', 'WT05_y', 
           'WT06_y', 'WT07_y', 'WT08_y', 'WT09_y', 'WT10_y', 'WT11_y', 'WT18_y',
           
           'WTSUMx', 'WTSUMy']
    
    X = data_copy[col_select]
    
    #### NORMALIZE X ####
    
    # Normalize so everything is on the same scale. 
    cols = X.columns
    # min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
    # Load it
    scaler = joblib.load('min_max_scaler.save')
    np_scaled = scaler.transform(X)
    
    # new data frame with the new scaled data. 
    X = pd.DataFrame(np_scaled, columns = cols)
    
    
    # 讀取gzip.Model
    with gzip.open('./grid.pgz', 'r') as xgbm2:
        xgb2 = pickle.load(xgbm2)
        pred = xgb2.predict(X)
        df_pred = pd.DataFrame(pred)

    return df_pred
        #future_pred = pd.concat([data_pred, df_pred], axis = 1)

        # future_pred.to_csv('future_pred.csv')


# file_name = sys.argv[1]
# predict_ans(file_name)

