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
highlighted_text2_col_up1 = "<span style='color: #56FF0D;'>T type customers both have cash and non-cash type credits. But G type customers are real individuals. So they only have cash limit and risk credits.</span>"
highlighted_text2_head_col_up1 = "<p style='color: #FFFFFF; font-size: 22px; font-style: bold'>Attributes defines the customer type</p>"
col_up1.markdown(highlighted_text2_head_col_up1, unsafe_allow_html=True)
col_up1.markdown(highlighted_text2_col_up1, unsafe_allow_html=True)

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

# creating a visualization over a column

# load the transaction history data
transaction_history = pd.read_feather('streamlit_view/transaction_history.feather')

# create header over the chart
st.subheader("Transactions have regular pattern except two days")
st.write("These two days are the first day of Bayram in Turkey. That's why they are days with the lowest transactions. You can observe check transaction dates from the chart below. Also, you are able to select a month")

# extract month-year values for the date filter based on months
transaction_history['MonthYear'] = transaction_history['ISLEM_TARIHI'].dt.to_period('M')
unique_months = transaction_history['MonthYear'].unique()

# creating a date filter for the transaction history using a select box (dropdown) component
selectbox_options = ['Whole Time Period'] + [month.strftime('%B') for month in unique_months]
selected_month = st.selectbox(' ',selectbox_options)

# filter the transaction history based on the selected month from the dropdown box
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

# adding two new containers for the next section
col_mid1, col_mid2 = st.columns(2)

# create a bar chart for customer frequency on the left container
customer_frequency = pd.read_feather('streamlit_view/customer_frequency.feather')       # load the view data
# add header and context first
col_mid1.subheader("Customers are Mostly Monthly or One-Timer ", anchor='center')

# changing values of the column to be more readable in the radio button filter
customer_frequency['SIRKET_TURU'] = customer_frequency['SIRKET_TURU'].replace(['G','T'],['Gerçek','Tüzel'],regex=True)
# then the radio button as the filter
sirket_turu_list = [str(item) for item in customer_frequency['SIRKET_TURU']]    # convert 'StringArray' column to a regular Python list to add the values into filter
sirket_turu_list = list(dict.fromkeys(sirket_turu_list))                        # drop duplicate values and keep only one from each
# create the radio button
filtered_sirket = col_mid1.radio("Filter by Company Type to Observe Changes on Frequency!", ['All'] + sirket_turu_list, horizontal= True)         # filter by company type value
if filtered_sirket != 'All':customer_frequency = customer_frequency[customer_frequency['SIRKET_TURU'] == filtered_sirket]

# calculate count of unique customers for each transactions frequency value to visualize in the chart
freq_counts = customer_frequency.groupby('TRANSACTIONS_FREQ')['MUSTERI_ID'].nunique().reset_index()
# replace the labels in the frequency column with the customized labels
label_mapping = {'One Timer': 'Only Visited Once','Rare': 'Rarely Visiting','Very Often': 'At Least Once a Month','Often':'Visiting in Every Three Months'}
freq_counts['TRANSACTIONS_FREQ'] = freq_counts['TRANSACTIONS_FREQ'].replace(label_mapping)

# visualize as a bar chart
transaction_freq_fig = go.Figure(data=go.Bar(x=freq_counts['MUSTERI_ID'],y=freq_counts['TRANSACTIONS_FREQ'],
        orientation='h',marker=dict(color='yellow'),text=freq_counts['MUSTERI_ID'],textposition='auto'))
# customize the layout
transaction_freq_fig.update_layout(xaxis_title='Unique Customer Count',yaxis_title='Transactions Frequency')
# render the bar chart
col_mid1.plotly_chart(transaction_freq_fig, use_container_width=True)

# create a line chart that represents distribution of the last transaction dates of the customers
last_transact = pd.read_feather('streamlit_view/last_transaction.feather')   # load the view data
# the context over the chart
last_transact_context="<p style='color: #4FFFE4; font-size: 16px; font-style: bold'>We keep track of our customers' frequency. This provides us to create a pattern about their risk. It is crucial to know their last visit as well to improve the pattern.This provides us to create a pattern about their risk. It is crucial to know their last visit as well to improve the pattern.</p>"
col_mid2.markdown(last_transact_context, unsafe_allow_html=True)
# and a headliner under the context
col_mid2.subheader("Most of the Customers Visited in the Last 30 Days")

# create a line chart for the last transaction dates on the right container
last_transact_fig = px.line(last_transact.value_counts('DAYS_SINCE_LAST_TRANSACTION').sort_index(ascending=True))
last_transact_fig.update_layout(xaxis_title='Days Since Last Transaction',yaxis_title='Number of Customers',
                showlegend=False)
last_transact_fig.update_traces(line=dict(color='#FF5C5C'))
# render the line chart
col_mid2.plotly_chart(last_transact_fig, use_container_width=True)

# creating tabs to navigate between charts of customer types
tabT, tabG = st.tabs(["Tüzel", "Şahıs"])
with tabT:
        st.markdown("<h2 style='font-style: italic;'>T Type Customers</h2>",unsafe_allow_html=True)

with tabG:
        st.markdown("<h2 style='font-style: italic;'>G Type Customers</h2>",unsafe_allow_html=True)

        tabG1, tabG2 = st.columns(2)    # create two containers for the next section

        # create a scatter plot chart for credit limit-risk
        bk_limitrisk = pd.read_feather('streamlit_view/bk_limit_risk_scatter.feather')       # load the view data
        sample_bk = bk_limitrisk.sample(1000)  # sample 1000 records to plot
        # visualize as a scatter chart
        scatter_bk = px.scatter(sample_bk,x=sample_bk['BK_LIMIT'],y=sample_bk['BK_RISK'])
        scatter_bk.update_traces(hovertemplate=None, hoverinfo='skip')
        scatter_bk.update_layout(xaxis_title="Credit Limit",yaxis_title="Credit Risk")
        # render the scatter chart
        tabG2.plotly_chart(scatter_bk, use_container_width=True)