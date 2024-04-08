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
# ===================================================================================
# ============================= Using Data ==========================================

FP1_ang_cols = {
    'PELVIS_ANGLE_X' : 'Pelvic_Anterior_Tilt',
    #'             ' : 'Pelvic_Up_(Obliquity)',
    #'             ' : 'Pelvic_Internal_Rotation',
    
    'FP1_HIP_ANGLE_X' : 'Hip_Flexion',
    'FP1_HIP_ANGLE_Y' : 'Hip_Adduction',
    'FP1_HIP_ANGLE_Z' : 'Hip_Internal_Rotation',
    
    'FP1_KNEE_ANGLE_X' : 'Knee_Flexion',
    #'               ' : 'Knee_Varus',
    #'               ' : 'Knee_Internal_Rotation',
    
    'FP1_ANKLE_ANGLE_X' : 'Ankle_Dorsiflexion',
    'FP1_ANKLE_ANGLE_Z' : 'Ankle_Inversion',
    
    #'RT_ANKLE_ANGLE_Y' : 'Ankle_Rotation',
    #'FP1_ANKLE_ANGLE_Y' : 'add',
    }

FP2_ang_cols = {
    'PELVIS_ANGLE_X' : 'Pelvic_Anterior_Tilt',
    #'              ' : 'Pelvic_Up_(Obliquity)',
    #'              ' : 'Pelvic_Internal_Rotation',
    
    'FP2_HIP_ANGLE_X' : 'Hip_Flexion',
    'FP2_HIP_ANGLE_Y' : 'Hip_Adduction',
    'FP2_HIP_ANGLE_Z' : 'Hip_Internal_Rotation',
    
    'FP2_KNEE_ANGLE_X' : 'Knee_Flexion',
    #'               ' : 'Knee_Varus',
    #'               ' : 'Knee_Internal_Rotation',
    
    'FP2_ANKLE_ANGLE_X' : 'Ankle_Dorsiflexion',
    'FP2_ANKLE_ANGLE_Y' : 'add',
    'FP2_ANKLE_ANGLE_Z' : 'Ankle_Inversion',
    
    #'RT_ANKLE_ANGLE_Y' : 'Ankle_Rotation',
    }

ap1_cols = {'FP1_FORCE_Y' : ['Stride Leg' , 'blue'],}
vt1_cols = {'FP1_FORCE_Z' : ['Stride Leg' , 'red'],}

ap2_cols = {'FP2_FORCE_Y' : ['Stride Leg', 'blue'],}
vt2_cols = {'FP2_FORCE_Z' : ['Stride Leg' , 'red'],}

FP1_mmt_cols = {
    'FP1_KNEE_MMT_X' : 'Knee_Medial_mmt',
    #'FP1_KNEE_MMT_Y' : 'Pelvic_Anterior_Tilt',
    #'FP1_KNEE_MMT_Z' : 'Pelvic_Anterior_Tilt',
    
    'FP1_ANKLE_MMT_X' : 'Ankle_Medial_mmt',
    #'FP1_ANKLE_MMT_Y' : 'Pelvic_Anterior_Tilt',
    #'FP1_ANKLE_MMT_Z' : 'Pelvic_Anterior_Tilt',
    }

FP2_mmt_cols = {
    'FP2_KNEE_MMT_X' : 'Knee_Medial_mmt',
    #'FP2_KNEE_MMT_Y' : 'Pelvic_Anterior_Tilt',
    #'FP2_KNEE_MMT_Z' : 'Pelvic_Anterior_Tilt',
    
    'FP2_ANKLE_MMT_X' : 'Ankle_Medial_mmt',
    #'FP2_ANKLE_MMT_Y' : 'Pelvic_Anterior_Tilt',
    #'FP2_ANKLE_MMT_Z' : 'Pelvic_Anterior_Tilt',
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
        elif 'MMT' in col:
            y_label = 'Moment [Nm/kg]'
        else:
            y_label = 'Angle [deg]'
        
        # Create the trace for the main data line
        trace = go.Scatter(x=time, y=df, mode='lines', name=cols[col], line=dict(color='orange'))
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

def grf_plotly(data, cols, time, k_Heel_contact_1, k_Toe_off_1, k_Heel_contact_2, k_Toe_off_2, axis):
    title = 'GROUND REACTION FORCE (AP-AXIS)' if axis == 'ap' else 'GROUND REACTION FORCE (Vertical)'
    
    y_values = {
        'max'       : {},
        'max_frame' : {},
        'min'       : {},
        'min_frame' : {},
        'k_Heel_contact_1'   : {},
        'k_Toe_off_1'        : {},
        'k_Heel_contact_2'   : {},
        'k_Toe_off_2'        : {},
    }
    
    # Create traces
    traces = []
    for col, info in cols.items():
        df = data[col]
        trace = go.Scatter(x=time, y=df, mode='lines', name=info[0], line=dict(color=info[-1]))
        traces.append(trace)
        
        # Perform and store the calculations for max, min and specific times
        y_values['k_Heel_contact_1'][col] = round(df[k_Heel_contact_1])
        y_values['k_Toe_off_1'][col]      = round(df[k_Toe_off_1])
        y_values['k_Heel_contact_2'][col] = round(df[k_Heel_contact_2])
        y_values['k_Toe_off_2'][col]      = round(df[k_Toe_off_2])
        
        y_values['max'][col]       = round(df.max(), 2)
        y_values['max_frame'][col] = np.where(df == df.max())[0][0]
        y_values['min'][col]       = round(df.min(), 2)
        y_values['min_frame'][col] = np.where(df == df.min())[0][0]
        
    # Adding reference lines and annotations
    reference_lines = []
    annotations = []

    # Add vertical lines and annotations for key events
    for key_time, description in zip([k_Heel_contact_1, k_Toe_off_1, k_Heel_contact_2, k_Toe_off_2],
                                    ['HC1', 'TO1', 'HC2', 'TO2']):
        reference_lines.append(
        go.Scatter(x=[time[key_time], time[key_time]], y=[df.min(), df.max()],
                    mode='lines', line=dict(color='black', width=2, dash='dash'),
                    showlegend=False)
    )
        annotations.append(
        dict(x=time[key_time], y=0.95, xref='x', yref='paper', showarrow=False,
                text=description,textangle=-90, bgcolor='rgba(0,0,0,0)', bordercolor='rgba(0,0,0,0)', borderwidth=0,
                )
    )

    # Update the layout with additional elements
    layout = go.Layout(
        title=title,
        xaxis=dict(title='Time [s]',
                    showgrid=False),
        yaxis=dict(
                    title='Force [% BW]',
                    showgrid=True,         # This will show the horizontal gridlines
                    gridcolor='lightgrey',
                    gridwidth=1,
                    zeroline=False
                ),
        showlegend=True,
        legend=dict(
                    x=1, # Adjust this value to move the legend left or right
                    y=1, # Adjust this value to move the legend up or down
                    xanchor='right', # Anchor the legend's right side at the x position
                    yanchor='top', # Anchor the legend's top at the y position
                    bgcolor='rgb(43,48,61)' # Set a background color with a bit of transparency
                    ),
        margin=dict(l=40, r=40, t=40, b=40),
        height=600,
        hovermode='closest',
        plot_bgcolor='rgb(43,48,61)',
        annotations=annotations
    )

    # Create the figure
    fig = go.Figure(data=traces + reference_lines, layout=layout)

    return fig, y_values

# ============================ 그래프 및 시점 수치 =======================================
FP1_values, FP1_fig = one_angle_plotly(fp1_filtered, FP1_ang_cols, fp_1time, k_Heel_contact_1, k_Toe_off_1, k_Heel_contact_2, k_Toe_off_2)
FP2_values, FP2_fig = one_angle_plotly(fp2_filtered, FP2_ang_cols, fp_2time, k_Heel_contact_1, k_Toe_off_1, k_Heel_contact_2, k_Toe_off_2)

force1_ap_fig, force1_ap_values = grf_plotly(fp1_filtered, ap1_cols, fp_1time, k_Heel_contact_1, k_Toe_off_1, k_Heel_contact_2, k_Toe_off_2, axis='ap')
force1_vt_fig, force1_vt_values = grf_plotly(fp1_filtered, vt1_cols, fp_1time, k_Heel_contact_1, k_Toe_off_1, k_Heel_contact_2, k_Toe_off_2, axis='vt')

force2_ap_fig, force2_ap_values = grf_plotly(fp2_filtered, ap2_cols, fp_2time, k_Heel_contact_1, k_Toe_off_1, k_Heel_contact_2, k_Toe_off_2, axis='ap')
force2_vt_fig, force2_vt_values = grf_plotly(fp2_filtered, vt2_cols, fp_2time, k_Heel_contact_1, k_Toe_off_1, k_Heel_contact_2, k_Toe_off_2, axis='vt')

FP1_mmt, mmt1_fig = one_angle_plotly(fp1_filtered, FP1_mmt_cols, fp_1time, k_Heel_contact_1, k_Toe_off_1, k_Heel_contact_2, k_Toe_off_2)
FP2_mmt, mmt2_fig = one_angle_plotly(fp2_filtered, FP2_mmt_cols, fp_2time, k_Heel_contact_1, k_Toe_off_1, k_Heel_contact_2, k_Toe_off_2)

# ===================================================================================

force1_ap_fig.update_layout(
    width=800,  # Set the width to your preference
    height=400  # Set the height to your preference
)
force1_vt_fig.update_layout(
    width=800,  # Set the width to your preference
    height=400  # Set the height to your preference
)

force2_ap_fig.update_layout(
    width=800,  # Set the width to your preference
    height=400  # Set the height to your preference
)
force2_vt_fig.update_layout(
    width=800,  # Set the width to your preference
    height=400  # Set the height to your preference
)

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
    
for col in mmt1_fig:
    fig = mmt1_fig[col]
    fig.update_layout(
        width=500,  # Desired width
        height=400,  # Desired height
        autosize=False  # Disable autosizing to enforce provided dimensions
    )
    
for col in mmt2_fig:
    fig = mmt2_fig[col]
    fig.update_layout(
        width=500,  # Desired width
        height=400,  # Desired height
        autosize=False  # Disable autosizing to enforce provided dimensions
    )
# ===================================================================================
# ============================= DashBoard ===========================================
st.title('KUM GAIT REPORT')

st.header('분석 구간')
st.image('image/analysis.png', use_column_width=True)

stride_length = round(fp1_filtered['stride_length'][0],2)
step_width = round(fp1_filtered['step_width'][0],2)

col1, col2 = st.columns(2)
col1.metric("Stride Length", f"{stride_length} cm", "height")
col2.metric("Step Width", f"{step_width} cm", "height")





st.subheader('KINEMATICS PARAMETERS')

tabs = st.tabs(FP1_ang_cols.values())

for tab, col_1, col_2 in zip(tabs, FP1_ang_cols, FP2_ang_cols):
    with tab:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.plotly_chart(FP1_fig[col_1], use_container_width=True)
        with col2:
            st.plotly_chart(FP2_fig[col_2], use_container_width=True)
        
# force
st.subheader('KINETICS PARAMETERS')

# 탭 생성
tab1, tab2 = st.tabs(["GRF AP axis", "GRF Verticla"])

with tab1:
    col1, col2 = st.columns([1, 1])  # 첫 번째 쌍의 차트를 위한 열 정의
    with col1:
        st.plotly_chart(force1_ap_fig, use_container_width=True)
    with col2:
        st.plotly_chart(force2_ap_fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns([1, 1])  # 두 번째 쌍의 차트를 위한 열 정의
    with col1:
        st.plotly_chart(force1_vt_fig, use_container_width=True)
    with col2:
        st.plotly_chart(force2_vt_fig, use_container_width=True)
        
# MMT
st.subheader('MOMENTS')
tabs = st.tabs(FP1_mmt_cols.values())

for tab, col_1, col_2 in zip(tabs, FP1_mmt_cols, FP2_mmt_cols):
    with tab:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.plotly_chart(mmt1_fig[col_1], use_container_width=True)
        with col2:
            st.plotly_chart(mmt2_fig[col_2], use_container_width=True)