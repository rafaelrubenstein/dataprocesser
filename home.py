import streamlit as st
import pandas as pd 
import numpy as np
from sklearn.preprocessing import StandardScaler,MinMaxScaler
import utils
from streamlit_extras.no_default_selectbox import selectbox



SHOW_DATASET = 'Show Dataset'

st.set_page_config(
    page_title="Data Processer",
    page_icon="📈",
    initial_sidebar_state="collapsed",
    layout = "centered",
)

st.write("Please upload the dataset")
uploaded_file = st.file_uploader("Choose a file", type=["csv","xlsx","json","html","sql"])

if uploaded_file is not None:
    if uploaded_file.type == "'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'":
        df = pd.read_excel(uploaded_file)

    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)

    if uploaded_file.type == "application/json":
        df = pd.read_json(uploaded_file)

    if uploaded_file.type == "text/html":
        df = pd.read_html(uploaded_file)

    if uploaded_file.type == "application/octet-stream":
        df = pd.read_sql(uploaded_file)

    option = selectbox("Choose what you want to do to the data",["Describe Data","Remove Nulls","Handle Categorical Data","Scale Features"])

    if option == "Describe Data":
        df_columns= df.columns.to_list()
        describe_option = selectbox("choose an option",['Describe Specific Column','Describe every column',SHOW_DATASET])
        if describe_option == 'Describe Specific Column':
            columns = st.multiselect("Which Columns would you like to describe?",df_columns,df_columns[0])
            utils.describe_specific_columnn(df,columns)
        if describe_option == 'Describe every column':
            utils.describe_all_columns(df)
        if describe_option == SHOW_DATASET:
            rows = st.number_input("how many rows?",min_value=5, key="numberofrows")
            st.write(df.head(rows))


    if option == "Remove Nulls":
        null_option = selectbox("choose an option",['Show Nulls',"Remove Columns",'Fill Null With Mean','Fill Null With Median','Fill Null With Mode',"Show Nulls after cleaning",SHOW_DATASET])
        if null_option == "Show Nulls":
            utils.show_nulls(df)
        if null_option == "Remove Columns":
            all_columns = st.checkbox("Click Here To Remove All Columns With Null Values")
            if all_columns:
                df = df.dropna(axis='columns')
            else:
                df_columns= df.columns.to_list()
                columns = st.multiselect("Which Columns would you like to remove?",df_columns)
                df = utils.remove_columns(df,columns)
        if null_option == 'Fill Null With Mean':
            all_columns = st.checkbox("Click Here To Fill All Columns with Mean")
            if all_columns:
                df = utils.fill_null(df,"mean",all_columns= True)
            else:
                df_columns= df.columns.to_list()
                columns = st.multiselect("Which Columns would you like to fill with mean?",df_columns)
                if len(columns) > 0:
                    df = utils.fill_null(df,'Mean',columns,all_columns)

                
        
        if null_option == 'Fill Null With Median':
            all_columns = st.checkbox("Click Here To Fill All Columns with Median")
            df_columns = df.columns.to_list()
            if all_columns:
                df = utils.fill_null(df,"median",all_columns= True)
            else:
                columns = st.multiselect("Which Columns would you like to fill with Median?",df_columns)
                if len(columns) > 0:
                    df = utils.fill_null(df,"median",columns,all_columns)
        
        if null_option == 'Fill Null With Mode':
            all_columns = st.checkbox("Click Here To Fill All Columns with Mode")
            if all_columns:
                df = utils.fill_null(df,"mode",all_columns= True)
            else:
                columns = st.multiselect("Which Columns would you like to fill with Mode?",df_columns)
                if len(columns) > 0:
                    df = utils.fill_null(df,'mode',columns,all_columns)

        if null_option == "Show Nulls after cleaning":
            utils.show_nulls(df)
        
        if null_option == SHOW_DATASET:
            rows = st.number_input("how many rows?",min_value=5, key="numberofrows")
            st.write(df.head(rows))

