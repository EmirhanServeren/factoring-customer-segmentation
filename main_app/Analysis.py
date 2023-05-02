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

import pyodbc           # importing for connecting to database
import json             # for reading the key inside the json formatted file

f = open('log.json')        # connection string to the database is available on the json file (but ignored in Github)
sql_key = json.load(f)      # returns JSON object as a dictionary

cnxn = pyodbc.connect(sql_key['key'])       # establish a connection
crsr = cnxn.cursor()                        # cursor enables to send command

# query for selecting necessary columns
viz_query= """SELECT MUSTERI_ID, KESIDECI_ID, CEK_NO, SIRKET_TURU, CEK_TUTAR, CEK_RENK, ISTIHBARAT_SONUC, MUSTERI_RISK_SEVIYESI FROM dbo.dataset """
visualization_df = pd.read_sql(viz_query, cnxn)

# create visualization for T/G type of companies
companyType_df = visualization_df[['MUSTERI_ID','SIRKET_TURU']]
companyType_df = companyType_df.drop_duplicates()
companyType_df = companyType_df['SIRKET_TURU'].value_counts()

# create visualization for çek renk
cek_color_df = visualization_df[['CEK_RENK']]
cek_color_df = cek_color_df['CEK_RENK'].value_counts()

# count number of MUSTERI and KESIDECI-> printing as metric with streamlit
customer_number = visualization_df[['MUSTERI_ID']]
customer_number = customer_number.drop_duplicates()     #customer_number.size

kesideci_number = visualization_df[['KESIDECI_ID']]
kesideci_number = kesideci_number.drop_duplicates()     #kesideci_number.size

# visualize "istihbarat sonucu"
# ...and make it a filter based on CEK_RENK
istihbarat_df=visualization_df[['CEK_NO','SIRKET_TURU','CEK_RENK','ISTIHBARAT_SONUC']]
istihbarat_df= istihbarat_df.drop_duplicates(subset='CEK_NO', keep="first")
#istihbarat_df= istihbarat_df['ISTIHBARAT_SONUC'].value_counts()

# VISUALIZATIONS-RELATED TO BK TAB (ŞAHIS TAB)
# query related attributes by filtering SIRKET_TURU as G (şahıs)
bk_query= """SELECT MUSTERI_ID, CEK_NO, BK_GECIKMEHESAP, 'BK_GECIKMEBAKIYE', BK_LIMIT, BK_RISK, BK_NOTU
                FROM dbo.dataset WHERE SIRKET_TURU LIKE 'G' """
visualization_bk_df = pd.read_sql(bk_query, cnxn)

sample_bk=visualization_bk_df.sample(n=1000)
# scatter the limit by risk
scatter_bklimitrisk = px.scatter(
    sample_bk[['BK_LIMIT','BK_RISK']],
    x="BK_LIMIT",
    y="BK_RISK",
)


# ----------------------------------------------
#   STARTING WEB-APP RELATED PARTS AFTER HERE
# ----------------------------------------------


# rename page name and set layout wider
st.set_page_config(page_title="Analytics Reporting",layout="wide")
st.header("Customer Reports-Analytics")     # create header for page

# create sidebar and other sub-page components here
st.sidebar.title("Customer Segmentation Capstone Project Web-App")
st.sidebar.write("Project by ENM and CMP students. Cansu Can, Derya Ekin Dereci, Eda Merduman from ENM Team and Emirhan Serveren, Mert Oğuz, Oğuz Alp Özçelik from CMP Team")

# put dummy text at first, ask ENM team to fill contexts
dummy_text="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc bibendum mollis nibh non rutrum. Orci varius natoque penatibus 
et magnis dis parturient montes, nascetur ridiculus mus. Curabitur vulputate volutpat rhoncus.
Maecenas aliquam ultrices placerat. Etiam venenatis odio ac nisl finibus blandit. Maecenas nec luctus dolor. 
In sagittis semper ligula, et pretium quam rutrum eget. Nullam vel ullamcorper risus.
Vestibulum hendrerit ante diam, a ultrices ipsum posuere id."""

# putting a context at first
st.write(dummy_text)

# create column containers of web page
col_up1,col_up2,col_up3=st.columns(3, gap="large")

# filling the containers
col_up1.write(dummy_text)   # left column
# middle column
col_up2.subheader("Şirket Türüne göre Dağılımı")
col_up2.bar_chart(companyType_df)
# right column
col_up3.metric(label="Verisetindeki girdi sayısı", value=str(visualization_df['MUSTERI_ID'].size))
col_up3.metric(label="Verisetindeki müşteri sayısı", value=str(customer_number.size))
col_up3.metric(label="Verisetindeki keşideci sayısı", value=str(kesideci_number.size))

# create another column containers of web page
col_down1,col_down2=st.columns(2, gap="large")
col_down1.subheader("Veri setindeki Çek Renklerinin Dağılımı")
col_down1.bar_chart(cek_color_df)
col_down1.write(" Çek rengi KKB tarafından bankalara aktarılan bir bilgidir. Açık Yeşilden Siyaha sıralanmıştır. Açık Yeşil kredibilitesi en yüksek çektir, siyaha geçtikçe çekin kredibilitesi düşmektedir.")
col_down2.write(dummy_text)
#cek_color_dropdown=col_down2.selectbox("çek rengi seçiniz",cek_color_df.index.tolist())
col_down2.subheader("Çeklerin İstihbarat Sonuçları")
col_down2.bar_chart(istihbarat_df['ISTIHBARAT_SONUC'].value_counts())

# creating tabs to navigate between charts of SIRKET_TURU T and G
tabT, tabG = st.tabs(["Tüzel Şirketler", "Şahıs Şirketleri"])
with tabT:
    st.header("Tüzel Şirketler")
    st.write(dummy_text)   # dummy text for now
with tabG:
    st.header("Şahıs Şirketleri")
    st.plotly_chart(scatter_bklimitrisk, theme=None, use_container_width=True)
    st.write(dummy_text)