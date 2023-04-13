# importing streamlit framework for deploying web-app
import streamlit as st

# importing libraries for data analysis
import pandas as pd
import numpy as np

import pyodbc           # importing for connecting to database
import json             # for reading the key inside the json formatted file

f = open('log.json')        # connection string to the database is available on the json file
sql_key = json.load(f)      # returns JSON object as a dictionary

cnxn = pyodbc.connect(sql_key['key'])       # establish a connection
crsr = cnxn.cursor()                        # cursor enables to send command

# query for selecting necessary columns
viz_query= """SELECT MUSTERI_ID, KESIDECI_ID, CEK_NO, SIRKET_TURU, CEK_TUTAR, CEK_RENK FROM dbo.dataset """
visualization_df = pd.read_sql(viz_query, cnxn)

# create visualization for T/G type of companies
companyType_df = visualization_df[['MUSTERI_ID','SIRKET_TURU']]
companyType_df = companyType_df.drop_duplicates()
companyType_df = companyType_df['SIRKET_TURU'].value_counts()

# create visualization for çek renk
cek_color_df = visualization_df[['MUSTERI_ID','CEK_RENK']]
cek_color_df = cek_color_df['CEK_RENK'].value_counts()

# count number of customers (MUSTERI)
customer_number = visualization_df[['MUSTERI_ID']]
customer_number = customer_number.drop_duplicates()
#customer_number.size

# rename page name
st.set_page_config(page_title="Analytics Page")

# create header for page
st.header("Customer Reports-Analytics")

# create sidebar and other sub-page components here
st.sidebar.title("Customer Segmentation Capstone Project Web-App")
st.sidebar.write("Project by ENM and CMP students. Cansu Can, Derya Ekin Dereci, Eda Merduman from ENM Team and Emirhan Serveren, Mert Oğuz, Oğuz Alp Özçelik from CMP Team")

# put dummy text at first, ask ENM team to fill contexts
dummy_text="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc bibendum mollis nibh non rutrum. Orci varius natoque penatibus 
et magnis dis parturient montes, nascetur ridiculus mus. Curabitur vulputate volutpat rhoncus.
Maecenas aliquam ultrices placerat. Etiam venenatis odio ac nisl finibus blandit. Maecenas nec luctus dolor. 
In sagittis semper ligula, et pretium quam rutrum eget. Nullam vel ullamcorper risus.
Vestibulum hendrerit ante diam, a ultrices ipsum posuere id."""

st.write(dummy_text)
st.write(f"{str(customer_number.size)} müşteri bulunmaktadır")
st.bar_chart(companyType_df)
st.bar_chart(cek_color_df)