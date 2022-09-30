import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Compare data sources",
    page_icon="🆚",
    layout="wide",
    initial_sidebar_state="auto"
)

def difference(measured, reanalysis):
    a = measured[measured != -999]
    b = reanalysis[measured != -999]
    return np.mean(abs(a-b))

def plot_two_series(variable, variables):
    data = pd.read_csv('Data/'+str(variables[variable]['code'])+'.csv')
    data['Data-Ora']= pd.to_datetime(data['Data-Ora'])
    measured = data.values[:,2]
    reanalysis = data.values[:,3]

    fig, ax = plt.subplots()
    ax.plot(data.values[:,1], reanalysis, '.', label ='Reanalysis')
    ax.plot(data.values[:,1], measured, '.', label = 'Measured')
    ax.set_xlabel('Time')
    ax.set_ylabel(variables[variable]['type'])
    ax.set_ylim(variables[variable]['min'],variables[variable]['max'])
    ax.text(0.05, 0.9, 'Mean abs difference = '+str(round(difference(measured, reanalysis),1)), transform=ax.transAxes)
    ax.text(0.05, 0.8, '# of no data = '+str(measured[measured==-999].shape[0]), transform=ax.transAxes)
    ax.legend()
    return fig

def plot_two_histograms(variable, variables):
    data = pd.read_csv('Data/'+str(variables[variable]['code'])+'.csv')
    data['Data-Ora']= pd.to_datetime(data['Data-Ora'])
    measured = data.values[:,2]
    reanalysis = data.values[:,3]

    fig, ax = plt.subplots()
    ax.hist(reanalysis[measured != -999], density = True, histtype = 'step', label ='Reanalysis')
    ax.hist(measured[measured != -999], density = True, histtype = 'step', label = 'Measured')
    ax.set_xlabel(variables[variable]['type'])
    ax.set_ylabel('Frequency')
    ax.legend()
    return fig


variables = {'Temperature Cassina Valsassina': {'code': 2146, 'type': 'Temperature [K]', 'max': 40, 'min': -10},
             'Temperature v.Sora': {'code': 10377, 'type': 'Temperature [K]', 'max': 40, 'min': -10},
             'Wind velocity Cassina Valsassina': {'code': 11647, 'type': 'Valocity [m/s]', 'max': 10, 'min': 0}}


r'''
# Measured data 🆚 Observed data

Here, a comparison between the data measured by ARPA Lombardia and the data 
produced by the reanalysis project COSMO 6 is performed. The objective 
is to assess the quality of the reanalysis data considering that the information 
measured by ARPA Lombardia is feasible.

'''

variable = st.selectbox('Select the variable you want to compare:', variables, 0)

col1,col2 = st.columns([2,2])

with col1:
    st.pyplot(plot_two_histograms(variable, variables))
with col2:
    st.pyplot(plot_two_series(variable, variables))