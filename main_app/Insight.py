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
st.markdown("<p style='color: #FF8585; font-size: 18px; font-style: italic'>Move forward with accurate decisions on the factoring business. Make data-oriented decisions for success. Learn insight into your customers. Discover facts.</p>", unsafe_allow_html=True)

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
col_up2.markdown("**Excess of G Type Customers are not preffered** in factoring business most of times.")
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


# create a header for the next section column
st.markdown("<h2 style='font-style: italic;'>Manage Your Customer Portfolio. Dive Into Your Greatest Asset. Time.</h2>",unsafe_allow_html=True)
# add a text under header
st.markdown("<p style='color: #FF8585; font-size: 18px; font-style: italic'>We provide insight into your relationships with your customers. By deriving new features using transaction dates, we create powerful analytics.</p>", unsafe_allow_html=True)

# load the transaction history data
transaction_history = pd.read_feather('streamlit_view/transaction_history.feather')
# create header over the chart
st.subheader("Transactions have regular pattern except two days")
st.markdown("**These two days are the first day of Bayram in Turkey.** That's why they are days with the lowest transactions. You can observe check transaction dates from the chart below. Also, you are able to select a month")
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
filtered_sirket = col_mid1.radio("T type customers mostly have monthly customers. G type generally has one-timer. Filter to Observe Changes!", ['All'] + sirket_turu_list, horizontal= True)         # filter by company type value
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
# the context over the chart declared first
last_transact_context="<p style='color: #4FFFE4; font-size: 16px; font-style: bold'>We keep track of our customers' frequency. This provides us to create a pattern about their risk. It is crucial to know their last visit as well to improve the pattern. </p>"
col_mid2.markdown(last_transact_context, unsafe_allow_html=True)
# and a headliner under the context
col_mid2.subheader("Most of the Customers Visited in the Last 30 Days")
# visualize the line chart for the last transaction dates on the right container
last_transact_fig = px.line(last_transact.value_counts('DAYS_SINCE_LAST_TRANSACTION').sort_index(ascending=True))
last_transact_fig.update_layout(xaxis_title='Days Since Last Transaction',yaxis_title='Number of Customers',
                showlegend=False)
last_transact_fig.update_traces(line=dict(color='#FF5C5C'), hovertemplate=None, hoverinfo='skip')
# render the line chart
col_mid2.plotly_chart(last_transact_fig, use_container_width=True)


# before declaring these columns, create a header for the new section
st.markdown("<h2 style='font-style: italic;'>Checks. Instruments of this Game.</h2>",unsafe_allow_html=True)
# add a text under header
st.markdown("<p style='color: #FF8585; font-style: italic; font-size: 18px;'>The check amount are already provided in data. However, not useful info without transforming it into meaningful result.</p>", unsafe_allow_html=True)

# create two new columns for the next section
col_down1, col_down2= st.columns(2)

# create bar chart for average check amount by KV/KY
cek_amount_by_KV_KY = pd.read_feather('streamlit_view/cek_tutar_by_kullandırım.feather')   # load the view data
# start with an header
col_down1.subheader("Accepted Checks Average Amount Doubles Denied Checks")
# visualize the bar chart
avg_cek_amount = cek_amount_by_KV_KY.groupby('KULLANDIRIM')['CEK_TUTAR'].mean()        # mean by group to find average
count_values = cek_amount_by_KV_KY.groupby('KULLANDIRIM')['CEK_TUTAR'].count()         # count to print on bars
avg_cek_amount.index=['Check Usage Denied','Usage Verified']                           # rename index values
fig_cek_amount = go.Figure(data=go.Bar(x=avg_cek_amount.index, y=avg_cek_amount, text= count_values))
fig_cek_amount.update_layout(yaxis_title='Average Check Amount')
cek_amount_colors = ['#FF1F1F', '#1FFF5E']
fig_cek_amount.update_traces(marker=dict(color=cek_amount_colors),hovertemplate=None, hoverinfo='skip')
# render the chart
col_down1.plotly_chart(fig_cek_amount, use_container_width=True)

# create a donut chart for distribution of KV/KY of the checks
companies_KV_KY = pd.read_feather('streamlit_view/companies_KV_KY_distribution.feather')   # load the view data
companies_KV_KY = companies_KV_KY['KULLANDIRIM'].value_counts()                            # count the number of checks by KV/KY
companies_KV_KY.index=['Check Usage Denied','Usage Verified']    # rename index values
# visualize KV/KY count as a donut chart
figure_company_KV_KY = go.Figure(data=[go.Pie(labels=companies_KV_KY.index,
        values=companies_KV_KY.values)])                # create a donut chart
figure_company_KV_KY.update_traces(hole=0.4, hovertemplate=None, hoverinfo='skip')    # set the hole size for the donut chart
figure_company_KV_KY.update_traces(marker=dict(colors=['#FF1F1F','#1FFF5E']))         # visualize KV with green and KY with red
# add a context under the donut chart
col_down2.subheader("Possible to see Supremacy of Denies due to Excess of G Type Customers")
# render the donut chart
col_down2.plotly_chart(figure_company_KV_KY, use_container_width=True)

# creating tabs to navigate between charts of customer types
tabG, tabT = st.tabs(["Şahıs", "Tüzel"])
with tabT:
        tabT1, tabT2 = st.columns(2)  # create two containers for the next section

        # header over the navigation tab
        tabT1.markdown("<h2 style='font-style: italic;'>G Type Customers</h2>",unsafe_allow_html=True)

        # denoted the context next to the chart
        tabT1.markdown("""<p style='color: #FFFF00; font-style: bold; font-size: 18px;'>The T Type Customers
                consideres corporations, comapnies and organizations.</p>""", unsafe_allow_html=True)
        tabT1.markdown("""<p style='color: #FFFFFF; font-style: bold; font-size: 18px;'>These customers
                are preferred customers on portfolio mostly.</p>""", unsafe_allow_html=True)
        tabT1.markdown("""<p style='color: #FFFF00; font-style: bold; font-size: 18px;'>By seperating them, can
                provide customized offers which fits their organization type.</p>""", unsafe_allow_html=True)
        tabT1.markdown("""<p style='color: #FFFFFF; font-style: bold; font-size: 18px;'>They can get
                both cash and non-cash type credits.</p>""", unsafe_allow_html=True)
        tabT1.markdown("""<p style='color: #FFFF00; font-style: bold; font-size: 18px;'>Non-cash type credit
                may be any non-cash meta that converted into valuable cash resource. Such as land registers and transport vehicles.</p>""", unsafe_allow_html=True)

        attribute = tabT2.selectbox('Navigate between cash and non-cash credit distributions', ['TK_NAKDILIMIT', 'TK_GAYRINAKDILIMIT'])

        # create a scatter plot chart for credit limit-risk
        tk_limitrisk = pd.read_feather('streamlit_view/tk_limit_risk_scatter.feather')  # Load T Type customer data
        if attribute == 'TK_NAKDILIMIT':
                x_attr = 'TK_NAKDILIMIT'
                y_attr = 'TK_NAKDIRISK'
        else:
                x_attr = 'TK_GAYRINAKDILIMIT'
                y_attr = 'TK_GAYRINAKDIRISK'
        sample_tk = tk_limitrisk.sample(1000)  # sample 1000 records to plot
        # visualize as a scatter chart
        scatter_tk = px.scatter(sample_tk, x=sample_tk[x_attr], y=sample_tk[y_attr])
        scatter_tk.update_traces(hovertemplate=None, hoverinfo='skip')
        scatter_tk.update_layout(xaxis_title="Credit Limit", yaxis_title="Credit Risk")
        # render the scatter chart
        tabT2.plotly_chart(scatter_tk, use_container_width=True)

with tabG:
        tabG1, tabG2 = st.columns(2)    # create two containers for the next section

        # header over the navigation tab
        tabG1.markdown("<h2 style='font-style: italic;'>G Type Customers</h2>",unsafe_allow_html=True)

        # denoted the context next to the chart
        tabG1.markdown("""<p style='color: #FFFF00; font-style: bold; font-size: 18px;'>The G Type Customers
                consideres real individuals and sole proprietorships.</p>""", unsafe_allow_html=True)
        tabG1.markdown("""<p style='color: #FFFFFF; font-style: bold; font-size: 18px;'>These customers
                are not preferred customers on portfolio mostly.</p>""", unsafe_allow_html=True)
        tabG1.markdown("""<p style='color: #FFFF00; font-style: bold; font-size: 18px;'>By segmenting them, can
                provide customized offers to them to reduce risk on this portfolio.</p>""", unsafe_allow_html=True)
        tabG1.markdown("""<p style='color: #FFFFFF; font-style: bold; font-size: 18px;'>They only can get
                cash type credits.</p>""", unsafe_allow_html=True)

        # create a scatter plot chart for credit limit-risk
        # header
        tabG2.markdown("<h3 style='font-style: italic;'>Credit Limit-Risk has a Trend over Customers</h3>", unsafe_allow_html=True)
        tabG2.markdown("<p style='font-size: 16px;'>The trend constructs pattern of segmentation model</p>", unsafe_allow_html=True)
        bk_limitrisk = pd.read_feather('streamlit_view/bk_limit_risk_scatter.feather')       # load the view data
        sample_bk = bk_limitrisk.sample(1000)  # sample 1000 records to plot
        # visualize as a scatter chart
        scatter_bk = px.scatter(sample_bk,x=sample_bk['BK_LIMIT'],y=sample_bk['BK_RISK'])
        scatter_bk.update_traces(hovertemplate=None, hoverinfo='skip')
        scatter_bk.update_layout(xaxis_title="Credit Limit",yaxis_title="Credit Risk")
        # render the scatter chart
        tabG2.plotly_chart(scatter_bk, use_container_width=True)