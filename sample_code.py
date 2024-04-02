import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st
import numpy as np
from glob import glob

KINEMATIC_PATH = 'data/**/kine/*csv'
FORCE_PATH = 'data/**/force/*csv'

KINEMATIC_DIR = [i.replace('\\','/') for i in glob(KINEMATIC_PATH)]
FORCE_DIR = [i.replace('\\','/') for i in glob(FORCE_PATH)]

kdf = pd.DataFrame()
fdf = pd.DataFrame()