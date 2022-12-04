import pandas as pd 
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import streamlit as st


def describe_specific_columnn(df,column_name):
    st.write(df[column_name].describe())

def describe_all_columns(df):
    st.write(df.describe())

def show_nulls(df):
    st.write(df.isna().sum())

def show_numeric_nulls_that_can_be_filled(df):
    null_columns = df.columns[df.isna().any()].tolist()
    st.write(df[null_columns].select_dtypes(include=np.number).columns.to_list())

def remove_columns(df,columns):
    df_copy= df.copy()
    df_copy.drop(columns=columns, inplace= True)
    return df_copy

def fill_null(df,method = None, columns= None, all_columns = False):
    if all_columns and method.lower() == 'mean':
        null_columns = df.columns[df.isna().any()].tolist()
        able_nulls = df[null_columns].select_dtypes(include=np.number).columns.to_list()
        mean = df[able_nulls].mean()
        df[able_nulls]= df[able_nulls].fillna(mean.iloc[0])
        return df
    if all_columns and method.lower() == 'median':
        null_columns = df.columns[df.isna().any()].tolist()
        able_nulls = df[null_columns].select_dtypes(include=np.number).columns.to_list()
        median = df[able_nulls].median()
        df[able_nulls]= df[able_nulls].fillna(median.iloc[0])
        return df
    if all_columns and method.lower() == 'mode':
        null_columns = df.columns[df.isna().any()].tolist()
        able_nulls = df[null_columns].select_dtypes(include=np.number).columns.to_list()
        mode = df[able_nulls].mode()
        df[able_nulls]= df[able_nulls].fillna(mode.iloc[0])
        return df
    try:
        if method.lower() == 'mean' and columns is not None:
            mean = df[columns].mean()
            df[columns] = df[columns].fillna(mean.iloc[0])
            return df
        elif method.lower() == 'mode' and columns is not None:
            mode = float(df[columns].mode())
            df[columns] = df[columns].fillna(mode.iloc[0])
            return df
        elif method.lower() == 'median' and columns is not None:
            median = df[columns].median()
            df[columns] = df[columns].fillna(median.iloc[0])
            return df
    except:
        print("Make sure column names were entered correctly")


def show_properties(df):
    return df.info()

def show_categorical_data(df):
    cat_columns =  df.select_dtypes(include=['object']).columns.to_list()
    unique = df[cat_columns].nunique()
    return unique

def perform_one_hot_encoding(df, columns):
    df = pd.get_dummies(df, columns=columns)
    return df

def scale_standard(df, columns = None, all_columns = False):
    df= df.copy()
    if all_columns:
        std_scaler =StandardScaler()
        df_scaled = std_scaler.fit_transform(df.to_numpy())
        df_scaled = pd.DataFrame(df_scaled, columns=df.columns.to_list())
        return df_scaled
    elif columns is not None:
        std_scaler =StandardScaler()
        df[columns] = std_scaler.fit_transform(df[columns].to_frame().to_numpy())
        return df
    else:
        print("make sure column input is correct")
    
def scale_min_max(df, columns = None, all_columns = False):
    df= df.copy()
    if all_columns:
        mm_scaler =MinMaxScaler()
        df_scaled = mm_scaler.fit_transform(df.to_numpy())
        df_scaled = pd.DataFrame(df_scaled, columns=df.columns.to_list())
        return df_scaled
    elif columns is not None:
        mm_scaler = MinMaxScaler()
        df[columns] = mm_scaler.fit_transform(df[columns].to_frame().to_numpy())
        return df
    else:
        print("make sure column input is correct")

def download_data(df,file_name = None):
    if file_name is None:
        print('No file Path Given')
    else:
        df.to_csv(file_name)