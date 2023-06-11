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

st.set_page_config(page_title="Analytics Reporting",layout="wide")      # rename page name and set layout wider

# create sidebar and other sub-page components here
st.sidebar.title("Customer Segmentation Capstone Project Web-App")
st.sidebar.write("Project by ENM and CMP students. Cansu Can, Derya Ekin Dereci, Eda Merduman from ENM Team and Emirhan Serveren, Mert Oğuz, Oğuz Alp Özçelik from CMP Team")

# create column containers of web page
col_up1,col_up2,col_up3=st.columns(3, gap="large")

# fill left container with text
col_up1.markdown("""The factoring company has an extensive customer portfolio. We examine
            them based on their **characteristic behaviors**. The analysis process starts with **dividing these customer
            group into two as G and T type customers**. Due to their differences, we perform analysis separately
            for each group. T type customers are the customers whom are legal entities (Tüzel Şirketler) and
            G type customers are the customers whom are real persons or companies (Gerçek Kişiler).""")

# fill middle container with chart
col_up2.subheader("There are G Type Customers Most Often", anchor='center')
# read the data from feather file and process
company_type_df=pd.read_feather('streamlit_view/company_type_distribution.feather')
# process data for visualization
company_type_df = company_type_df['SIRKET_TURU'].value_counts()
company_type_df.index=['Gerçek','Tüzel']    # rename index values
# create a donut chart for company type distribution
hovertemplate_company = "%{label} kişilerde %{value} çek kaydı bulunmaktadır<extra></extra>"
figure_companyType = go.Figure(data=[go.Pie(labels=company_type_df.index, values=company_type_df.values,
        hovertemplate=hovertemplate_company,
        hoverlabel=dict(align='left', font=dict(size=12)))])                # create a donut chart
figure_companyType.update_traces(hole=0.4)                                  # set the hole size for the donut chart
figure_companyType.update_layout(legend=dict(orientation="h", yanchor="bottom",
                        y=1.02, xanchor="center", x=0.5))
# render the donut chart
col_up2.plotly_chart(figure_companyType, use_container_width=True)

# fill right container with metrics
# ...

transaction_history = pd.read_feather('streamlit_view/transaction_history.feather')
# plot the count of records from dates as line chart
transaction_history_line = px.line(transaction_history.groupby('ISLEM_TARIHI')['ID'].count(),
            x=transaction_history.groupby('ISLEM_TARIHI')['ID'].count().index,
            y=transaction_history.groupby('ISLEM_TARIHI')['ID'].count().values,
            title='Çek Kayıtlarının Tarih Dağılımı')
transaction_history_line.update_layout(xaxis_title='Date', yaxis_title='Number of Records')
st.plotly_chart(transaction_history_line , use_container_width=True)