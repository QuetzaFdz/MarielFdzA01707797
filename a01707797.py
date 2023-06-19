import streamlit as st
import pandas as pd
import numpy as np
import plotly as px
import plotly.figure_factory as ff
from bokeh.plotting import figure
import matplotlib.pyplot as plt

st.title(':red[Police Incident Reports from 2018 to 2020 in San Francisco]')

df = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")

st.markdown('The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location and resolution.')

mapa = pd.DataFrame()
mapa['Date'] = df['Incident Date']
mapa['Day'] = df['Incident Day of Week']
mapa['Police District'] = df['Police District']
mapa['Neighborhood'] = df['Analysis Neighborhood']
mapa['Incident Category'] = df['Incident Category']
mapa['Incident Subcategory'] = df['Incident Subcategory']
mapa['Year'] = df['Incident Year']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']
mapa['Incident Day'] = df['Incident Day of Week']
mapa['Incident Type'] = df['Report Type Description']
mapa['Report Type'] = df['Report Type Code']
mapa['Hour'] = df['Incident Time']
mapa['Report Datetime'] = df['Report Datetime']
mapa = mapa.dropna()


subset_data3=mapa
police_district_input = st.sidebar.multiselect(
'Choose the year',
mapa.groupby('Year').count().reset_index()['Year'].tolist())
if len(police_district_input) > 0:
    subset_data2 = mapa[mapa['Year'].isin(police_district_input)]

subset_data2 = mapa
police_district_input = st.sidebar.multiselect(
'Police District',
mapa.groupby('Police District').count().reset_index()['Police District'].tolist())
if len(police_district_input) > 0:
    subset_data2 = mapa[mapa['Police District'].isin(police_district_input)]

subset_data1 = subset_data2
neighborhood_input = st.sidebar.multiselect(
'Neighborhood',
subset_data2.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist())
if len(neighborhood_input) > 0:
    subset_data1 = subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]

subset_data = subset_data1
incident_input = st.sidebar.multiselect(
'Incident Category',
subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
if len(incident_input) > 0:
    subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]
            
subset_data

st.markdown('It is important to mention that any police district can answer to any incident, the neighborhood in which it happened is not related to the police district.')    
st.markdown('**Crime locations in San Francisco**')
st.map(subset_data)
st.markdown('**Crimes ocurred per Police District**')
st.bar_chart(subset_data['Police District'].value_counts())
st.markdown('**Crimes ocurred per date**')
st.line_chart(subset_data['Date'].value_counts())
st.markdown('**Time in which the crime is executed**')
st.line_chart(subset_data['Report Datetime'].value_counts())
st.markdown('**Type of crimes committed**')
st.bar_chart(subset_data['Incident Category'].value_counts())
st.markdown('**Day of the week with the highest incidences**')
st.bar_chart(subset_data['Incident Day'].value_counts())
st.markdown('**Incident type**')
fig2, ax2 = plt.subplots()
labels = subset_data['Incident Type'].unique()
ax2.pie(subset_data['Incident Type'].value_counts(), labels=labels, autopct='%1.1f%%', startangle=20)
st.pyplot(fig2)
st.markdown('**Report Type**')
fig3, ax3 = plt.subplots()
labels = subset_data['Report Type'].unique()
ax3.pie(subset_data['Report Type'].value_counts(), labels=labels, autopct='%1.1f%%', startangle=20)
st.pyplot(fig3)
st.markdown('**Time when most incidents occur**')
st.line_chart(subset_data['Hour'].value_counts())


agree = st.button('Click to see Incident Subcategories')
if agree:
    st.markdown('Subtype of crimes committed')
    st.bar_chart(subset_data['Incident Subcategory'].value_counts())


st.markdown('**Resolution status**')
fig1, ax1 = plt.subplots()
labels = subset_data['Resolution'].unique()
ax1.pie(subset_data['Resolution'].value_counts(), labels=labels, autopct='%1.1f%%', startangle=20)
st.pyplot(fig1)