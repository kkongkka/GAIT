import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st
import numpy as np
from glob import glob
import data_concat

st.set_page_config(layout="wide")
@st.cache_data
def load_data():
    kdf, fdf = data_concat.data_concat()
    return kdf, fdf

kdf, fdf = load_data()

kdf['trial'] = kdf['trial'].astype(int)
fdf['trial'] = fdf['trial'].astype(int)

# 스트림릿 사이드바 설정
unique_names = kdf['player'].unique()
selected_name = st.sidebar.selectbox('Select Name', unique_names)
filtered_df_by_name = kdf[kdf['player'] == selected_name]
unique_dates = sorted(filtered_df_by_name['day'].unique())
selected_date = st.sidebar.selectbox('Select Date', unique_dates)

filtered_df_by_name_datas = kdf[(kdf['player'] == selected_name) &
                                (kdf['day'] == selected_date)]
unique_trial = sorted(filtered_df_by_name_datas['trial'].unique())
selected_trial = st.sidebar.selectbox('Select Date', unique_trial)

kine_filtered = kdf[(kdf['player'] == selected_name) & 
                    (kdf['day'] == selected_date) &
                    (kdf['trial'] == selected_trial)]

force_filtered = fdf[(fdf['player'] == selected_name) & 
                    (fdf['day'] == selected_date) &
                    (fdf['trial'] == selected_trial)]

kine_filtered.reset_index(inplace=True, drop=True)
force_filtered.reset_index(inplace=True, drop=True)

k_sr = 60
k_Heel_contact_1  = round(kine_filtered['Heel_contact_1'][0])
k_Toe_off_1       = round(kine_filtered['Toe_off_1'][0]      - k_Heel_contact_1)
k_Heel_contact_2  = round(kine_filtered['Heel_contact_2'][0] - k_Heel_contact_1)
k_Toe_off_2       = round(kine_filtered['Toe_off_2'][0]      - k_Heel_contact_1)
#stride_length = round(kine_filtered['stride_length'][0])

f_sr = 2160
f_Heel_contact_1  = round(force_filtered['Heel_contact_1'][0])
f_Toe_off_1       = round(force_filtered['Toe_off_1'][0]      - f_Heel_contact_1)
f_Heel_contact_2  = round(force_filtered['Heel_contact_2'][0] - f_Heel_contact_1)
f_Toe_off_2       = round(force_filtered['Toe_off_2'][0]      - f_Heel_contact_1)

k_foot_1 = kine_filtered.iloc[k_Heel_contact_1:int(k_Toe_off_1 + k_Heel_contact_1 + (k_sr * 0.2)),:].reset_index(drop=True)
f_foot_1 = force_filtered.iloc[f_Heel_contact_1:int(f_Toe_off_1 + f_Heel_contact_1 + (f_sr * 0.2)),:].reset_index(drop=True)

k_foot_2 = kine_filtered.iloc[k_Heel_contact_2:int(k_Toe_off_2 + k_Heel_contact_2 + (k_sr * 0.2)),:].reset_index(drop=True)
f_foot_2 = force_filtered.iloc[f_Heel_contact_2:int(f_Toe_off_2 + f_Heel_contact_2 + (f_sr * 0.2)),:].reset_index(drop=True)

k_foot_1.drop(['Heel_contact_1','Toe_off_1','Heel_contact_2','Toe_off_2'], axis=1, inplace=True)
f_foot_1.drop(['Heel_contact_1','Toe_off_1','Heel_contact_2','Toe_off_2'], axis=1, inplace=True)

k_foot_2.drop(['Heel_contact_1','Toe_off_1','Heel_contact_2','Toe_off_2'], axis=1, inplace=True)
f_foot_2.drop(['Heel_contact_1','Toe_off_1','Heel_contact_2','Toe_off_2'], axis=1, inplace=True)

k1_len = len(k_foot_1)
k1_time = np.arange(0,k1_len/k_sr, 1/k_sr)
k_1time = k1_time.round(3)

f1_len = len(f_foot_1)
f1_time = np.arange(0,f1_len/f_sr, 1/f_sr)
f1_time = f1_time.round(3)

k2_len = len(k_foot_2)
k2_time = np.arange(0,k2_len/k_sr, 1/k_sr)
k2_time = k2_time.round(3)

f2_len = len(f_foot_2)
f2_time = np.arange(0,f2_len/f_sr, 1/f_sr)
f2_time = f2_time.round(3)

# ===================================================================================
# ============================= Using Data ==========================================













# ============================ 그래프 및 시점 수치 =======================================
st.header('분석 구간')
st.image('image/analysis.png', use_column_width=True)