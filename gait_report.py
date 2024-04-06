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
    fp1, fp2 = data_concat.data_concat()
    return fp1, fp2

fp1, fp2 = load_data()

fp1['trial'] = fp1['trial'].astype(int)
fp2['trial'] = fp2['trial'].astype(int)

# 스트림릿 사이드바 설정
unique_names = fp1['player'].unique()
selected_name = st.sidebar.selectbox('Select Name', unique_names)
filtered_df_by_name = fp1[fp1['player'] == selected_name]
unique_dates = sorted(filtered_df_by_name['day'].unique())
selected_date = st.sidebar.selectbox('Select Date', unique_dates)

filtered_df_by_name_datas = fp1[(fp1['player'] == selected_name) &
                                (fp1['day'] == selected_date)]
unique_trial = sorted(filtered_df_by_name_datas['trial'].unique())
selected_trial = st.sidebar.selectbox('Select Date', unique_trial)

fp1_filtered = fp1[(fp1['player'] == selected_name) & 
                    (fp1['day'] == selected_date) &
                    (fp1['trial'] == selected_trial)]

fp2_filtered = fp2[(fp2['player'] == selected_name) & 
                    (fp2['day'] == selected_date) &
                    (fp2['trial'] == selected_trial)]

fp1_filtered.reset_index(inplace=True, drop=True)
fp2_filtered.reset_index(inplace=True, drop=True)

k_sr = 60; f_sr = 2160

k_Heel_contact_1  = fp1_filtered[round(fp1_filtered['k_Heel_contact_1'][0],) == round(fp1_filtered['FRAMES'],2)].index.tolist()
k_Toe_off_1       = fp1_filtered[round(fp1_filtered['k_Toe_off_1'][0],) == round(fp1_filtered['FRAMES'],2)].index.tolist()
k_Heel_contact_2  = fp2_filtered[round(fp2_filtered['k_Heel_contact_2'][0],) == round(fp2_filtered['FRAMES'],2)].index.tolist()
k_Toe_off_2       = fp2_filtered[round(fp2_filtered['k_Toe_off_2'][0],) == round(fp2_filtered['FRAMES'],2)].index.tolist()

fp1_filtered.drop(['k_Heel_contact_1','k_Toe_off_1','k_Heel_contact_2','k_Toe_off_2','f_Heel_contact_1','f_Toe_off_1','f_Heel_contact_2','f_Toe_off_2'], axis=1, inplace=True)
fp2_filtered.drop(['k_Heel_contact_1','k_Toe_off_1','k_Heel_contact_2','k_Toe_off_2','f_Heel_contact_1','f_Toe_off_1','f_Heel_contact_2','f_Toe_off_2'], axis=1, inplace=True)

fp1_len = len(fp1_filtered)
fp1_time = np.arange(0,fp1_len/k_sr, 1/k_sr)
fp_1time = fp1_time.round(3)

fp2_len = len(fp2_filtered)
fp2_time = np.arange(0,fp2_len/k_sr, 1/k_sr)
fp_2time = fp2_time.round(3)

ang_cols = {
    'PELVIS_ANGLE_X' : 'Pelvic_Anterior_Tilt',
    #'              ' : 'Pelvic_Up_(Obliquity)',
    #'              ' : 'Pelvic_Internal_Rotation',
    
    'RT_HIP_ANGLE_X' : 'Hip_Flexion',
    'RT_HIP_ANGLE_Y' : 'Hip_Adduction',
    'RT_HIP_ANGLE_Z' : 'Hip_Internal_Rotation',
    
    'RT_KNEE_ANGLE_X' : 'Knee_Flexion',
    #'               ' : 'Knee_Varus',
    #'               ' : 'Knee_Internal_Rotation',
    
    'RT_ANKLE_ANGLE_X' : 'Ankle_Dorsiflexion',
    'RT_ANKLE_ANGLE_Y' : 'add',
    'RT_ANKLE_ANGLE_Z' : 'Ankle_Inversion',
    
    #'RT_ANKLE_ANGLE_Y' : 'Ankle_Rotation',
    }

def one_angle_plotly(data, cols, time, k_Heel_contact_1, k_Toe_off_1, k_Heel_contact_2, k_Toe_off_2):
    ang = {
        'max'       : {},
        'max_frame' : {},
        'min'       : {},
        'min_frame' : {},
        'k_Heel_contact_1'   : {},
        'k_Toe_off_1'        : {},
        'k_Heel_contact_2'   : {},
        'k_Toe_off_2'        : {},
    }
    
    figures = {}
    
    for col in cols:
        df = data[col]
        if 'VELOCITY' in col:
            y_label = 'Angular Velocity [deg/s]'
        else:
            y_label = 'Angle [deg]'
        
        # Create the trace for the main data line
        trace = go.Scatter(x=time, y=df, mode='lines', name=cols[col], line=dict(color='firebrick'))
        traces = [trace]
        
        ang['k_Heel_contact_1'][col] = round(df[k_Heel_contact_1])
        ang['k_Toe_off_1'][col]      = round(df[k_Toe_off_1])
        ang['k_Heel_contact_2'][col] = round(df[k_Heel_contact_2])
        ang['k_Toe_off_2'][col]      = round(df[k_Toe_off_2])
        
        ang['max'][col]       = round(df.max(), 2)
        ang['max_frame'][col] = np.where(df == df.max())[0][0]
        ang['min'][col]       = round(df.min(), 2)
        ang['min_frame'][col] = np.where(df == df.min())[0][0]
        
        reference_lines =[]
        annotations = []
        
        for key_time, description in zip([k_Heel_contact_1, k_Toe_off_1, k_Heel_contact_2, k_Toe_off_2],
                                     ['HC1', 'TO1', 'HC2', 'TO2']):
            
            # 참조선
            reference_lines.append(
            go.Scatter(x=[time[key_time], time[key_time]], y=[df.min(), df.max()],
                       mode='lines', line=dict(color='black', width=2, dash='dash'),
                       showlegend=False)
        )
            # 주석
            annotations.append(
            dict(x=time[key_time], y=0.95, xref='x', yref='paper', showarrow=False,
                 text=description,textangle=-90, bgcolor='rgba(0,0,0,0)', bordercolor='rgba(0,0,0,0)', borderwidth=0,
                 )
        )
        
        # Define the layout
        layout = go.Layout(
            title=f'{cols[col]}',
            xaxis=dict(title='Time [s]',
                       showgrid=False),
            yaxis=dict(title=y_label,
                       autorange = True,
                       rangemode='tozero',
                        showgrid=True,         # This will show the horizontal gridlines
                        gridcolor='lightgrey',
                        gridwidth=1,
                        zeroline=False,
                        ),                        
            showlegend=False,
            margin=dict(l=40, r=40, t=40, b=40),
            height=400,
            plot_bgcolor='rgb(43,48,61)',
            annotations=annotations
        )
        
        # Create the figure and add the traces to it
        fig = go.Figure(data=traces + reference_lines, layout=layout)
        
        # Store the figure in the dictionary
        figures[col] = fig
        
    return ang, figures

FP1_values, FP1_fig = one_angle_plotly(fp1_filtered, ang_cols, fp_1time, k_Heel_contact_1, k_Toe_off_1, k_Heel_contact_2, k_Toe_off_2)
FP2_values, FP2_fig = one_angle_plotly(fp2_filtered, ang_cols, fp_2time, k_Heel_contact_1, k_Toe_off_1, k_Heel_contact_2, k_Toe_off_2)

for col in FP1_fig:
    fig = FP1_fig[col]
    fig.update_layout(
        width=500,  # Desired width
        height=400,  # Desired height
        autosize=False  # Disable autosizing to enforce provided dimensions
    )

for col in FP2_fig:
    fig = FP2_fig[col]
    fig.update_layout(
        width=500,  # Desired width
        height=400,  # Desired height
        autosize=False  # Disable autosizing to enforce provided dimensions
    )
    
st.header('분석 구간')
st.image('image/analysis.png', use_column_width=True)

st.subheader('KINEMATICS PARAMETERS')

st.write("GROUND REACTION FORCE AP")

for col in ang_cols:
    st.write(ang_cols[col])

    # Create two columns with equal width
    col1, col2 = st.columns([1, 1])

    with col1:
        # Render the FP1_fig graph in the left column
        st.plotly_chart(FP1_fig[col], use_container_width=True)

    with col2:
        # Render the FP2_fig graph in the right column
        st.plotly_chart(FP2_fig[col], use_container_width=True)

