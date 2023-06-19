# importing streamlit framework for deploying web-app
import streamlit as st
# for altair charts in streamlit library
import altair as alt
# importing libraries for data analysis
import pandas as pd
import numpy as np
# importing to visualization where streamlit is not enough
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# rename page name
st.set_page_config(page_title="Customer Segmentation",layout="wide")

# create a header for web page
st.markdown("<h1 style='font-style: italic;'>Data-Oriented Perspective. Provides Reliability.</h1>",unsafe_allow_html=True)
# add a text under header
st.markdown("<p style='color: #FF8585; font-size: 18px; font-style: bold'>Observe our Customer Segmentation model. Powered with Business Intelligence. Create rapid and smart strategies for your customers. </p>", unsafe_allow_html=True)

# create sidebar and other sub-page components here
st.sidebar.title("Customer Segmentation Capstone Project Web-App")
st.sidebar.write("Project by ENM and CMP students. Cansu Can, Derya Ekin Dereci, Eda Merduman from ENM Team and Emirhan Serveren, Mert Oğuz, Oğuz Alp Özçelik from CMP Team")

# create column containers for the upper section
col_up, col_up_2, col_up_3 = st.columns(3)

# create a header over visualization first
col_up_2.subheader("Factoring Labeled %90 of Customers as Very Reliable")
col_up_2.write("Meanwhile %75 of Checks are Denied for Usage")
# visualize MUSTERI_RISK_SEVIYESI on the first section
risk_level = pd.read_feather("streamlit_view/risk_level.feather") # load data
# create a bar chart visualization
risk_level_fig = go.Figure(data=go.Bar(x=risk_level["index"], y=risk_level["MUSTERI_RISK_SEVIYESI"],
                marker=dict(color="yellow"), text=risk_level["MUSTERI_RISK_SEVIYESI"], textposition='auto'))
risk_level_fig.update_layout(xaxis_title="Risk Level (Defined by Corporation)", yaxis_title="Number of Customers",
                xaxis={'type': 'category', 'categoryorder': 'array', 'categoryarray': risk_level["index"]},     # to print all values in index
                showlegend=False)
risk_level_fig.update_traces(hovertemplate=None, hoverinfo='skip')                                              # close tooltip feature
# render the chart
col_up_2.plotly_chart(risk_level_fig, use_container_width=True)


# create column containers for the next section
col_1, col_2 = st.columns(2)

# create a donut chart for distribution of segments
bk_cluster_distribution = pd.read_feather('streamlit_view/bk_cluster_distribution')
# header and context at the top
col_1.subheader("Observe the Segment Distribution")
# visualize here
fig_bk_distribution = go.Figure(data=[go.Pie(labels=bk_cluster_distribution['Segment'],
                values=bk_cluster_distribution['Count'])])
fig_bk_distribution.update_traces(hole=0.4, hovertemplate=None, hoverinfo='skip')
# render the chart
col_1.plotly_chart(fig_bk_distribution, use_container_width=True)

# print the numerical visualization right to the chart as a data frame
bk_cluster_distribution= bk_cluster_distribution.rename(columns={'Count':'Number of Customers'})
col_2.dataframe(bk_cluster_distribution.set_index('Segment'), use_container_width=True)

# create another column containers for the next section
column_1,column_2,column_3 = st.columns(3)

# header declared first because it is over the chart
column_2.subheader("Reliable Segment has More Income and Less Loss from Checks")
# check income-loss percentage chart which is on the left container
bk_check_income = pd.read_feather("streamlit_view/bk_cluster_check_income.feather")
# create the visualization below
fig_bk_check_income = go.Figure(data=[
    go.Bar(name='Check Income (%)', x=bk_check_income['Segment'], y=bk_check_income['Check Income (%)'],
        text=bk_check_income['Check Income (%)'].round(2), textposition='auto', marker=dict(color='yellow')),
    go.Bar(name='Check Loss (%)', x=bk_check_income['Segment'], y=bk_check_income['Check Loss (%)'],
        text=bk_check_income['Check Loss (%)'].round(2), textposition='auto', marker=dict(color='red'))])
# then declare the stack mode
fig_bk_check_income.update_layout(xaxis_title=None,yaxis_title='Percentage (%)', barmode='stack')
fig_bk_check_income.update_traces(hovertemplate=None, hoverinfo='skip')
# render the chart
column_2.plotly_chart(fig_bk_check_income, use_container_width=True)
