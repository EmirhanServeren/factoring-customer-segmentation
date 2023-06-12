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
# for transaction history chart date filter
import calendar

# rename page name and set layout wider
st.set_page_config(page_title="Analytics Reporting",layout="wide")

# create a header for web page
st.markdown("<h1 style='font-style: italic;'>Know Your Customers. Lead Your Business.</h1>",unsafe_allow_html=True)
# add a text under header
st.markdown("<p style='color: #FF8585; font-size: 18px; font-style: bold'>Move forward with accurate decisions on the factoring business. Make data-oriented decisions for success. Learn insight into your customers. Discover facts.</p>", unsafe_allow_html=True)

# create sidebar and other sub-page components here
st.sidebar.title("Customer Segmentation Capstone Project Web-App")
st.sidebar.write("Project by ENM and CMP students. Cansu Can, Derya Ekin Dereci, Eda Merduman from ENM Team and Emirhan Serveren, Mert Oğuz, Oğuz Alp Özçelik from CMP Team")

# create column containers of web page
col_up1,col_up2,col_up3=st.columns(3)

# fill left container with text
col_up1_markdown_text = """The factoring company has an extensive customer portfolio. We examine them based on their **characteristic behaviors**. 
The analysis process starts with dividing these customer group into two as G and T type customers.
Due to their differences, we perform analysis separately for each group. T type customers are the customers whom are legal entities *(Tüzel Şirketler)*
and G type customers are the customers whom are real persons or companies *(Gerçek Kişiler)*."""
# highlight the sentence with a yellow color
highlighted_text_col_up1 = "<span style='color: yellow;'>Due to their differences, we perform analysis separately for each group.</span>"
markdown_text = col_up1_markdown_text.replace("Due to their differences, we perform analysis separately for each group.", highlighted_text_col_up1)
# write the text to the container
col_up1.markdown(markdown_text, unsafe_allow_html=True)

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
metrics = pd.read_feather('streamlit_view/metrics.feather')
col_up3.metric(label="Total Transactions", value=str(metrics['ID'].nunique()))
col_up3.metric(label="Number of Customers Worked With", value=str(metrics['MUSTERI_ID'].nunique()))
col_up3.metric(label="Number of Drawer that Customers Worked With", value=str(metrics['KESIDECI_ID'].nunique()))
col_up3.metric(label="Total Number of Checks", value=str(metrics['CEK_NO'].nunique()))
col_up3.metric(label="Number of Branches that Checks Operated", value=str(metrics['SUBE'].nunique()))

# create column containers of web page
# load the transaction history data
transaction_history = pd.read_feather('streamlit_view/transaction_history.feather')
# extract month-year values for the date filter based on months
transaction_history['MonthYear'] = transaction_history['ISLEM_TARIHI'].dt.to_period('M')
unique_months = transaction_history['MonthYear'].unique()
# creating a date filter for the transaction history
selectbox_options = ['Whole Time Period'] + [month.strftime('%B') for month in unique_months]
selected_month = st.selectbox('You can observe check transaction dates from the chart below. Also, you are able to select a month ', 
                selectbox_options)
# filter the transaction history based on the selected month
if selected_month == 'Whole Time Period': filtered_data = transaction_history     # for the case all months are considered
else:
        selected_month_idx = selectbox_options.index(selected_month)
        selected_month_value = unique_months[selected_month_idx - 1]
        filtered_data = transaction_history[transaction_history['MonthYear'] == selected_month_value]
# plot the count of records from dates as a line chart
transaction_history_line = px.line(filtered_data.groupby('ISLEM_TARIHI')['ID'].count(),
                x=filtered_data.groupby('ISLEM_TARIHI')['ID'].count().index,
                y=filtered_data.groupby('ISLEM_TARIHI')['ID'].count().values)
# updating the chart axis and tooltip
transaction_history_line.update_layout(xaxis_title='Date', yaxis_title='Number of Records')
transaction_history_line.update_traces(hovertemplate="There are %{y} records on %{x}")
# render the line chart
st.plotly_chart(transaction_history_line, use_container_width=True)

col_mid1, col_mid2 = st.columns(2)

# will fill these containers with charts
# ...
