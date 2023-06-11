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

# query for selecting necessary columns
viz_query= """SELECT MUSTERI_ID, KESIDECI_ID, CEK_NO, SIRKET_TURU, CEK_TUTAR, CEK_RENK, ISTIHBARAT_SONUC, MUSTERI_RISK_SEVIYESI FROM dataset """
visualization_df = pd.read_sql(viz_query, cnxn)

# create visualization for risk seviyesi
riskLevel_df = visualization_df[['MUSTERI_ID','MUSTERI_RISK_SEVIYESI']]
riskLevel_df = riskLevel_df.drop_duplicates(subset='MUSTERI_ID', keep='first')      # drop duplicate IDs to count
riskLevel_df = riskLevel_df['MUSTERI_RISK_SEVIYESI'].value_counts()

# create visualization for T/G type of companies
companyType_df = visualization_df[['MUSTERI_ID','SIRKET_TURU']]
companyType_df = companyType_df.drop_duplicates(subset='MUSTERI_ID', keep='first')      # drop duplicate IDs to count the number of companies accurately
companyType_df = companyType_df['SIRKET_TURU'].value_counts()
# define a dictionary to map original labels to renamed kişi tipi (T/G) labels
companyType_label_mapping = {'T': 'Tüzel','G':'Gerçek'}
companyType_df = companyType_df.rename(index=companyType_label_mapping)     # rename the labels using the mapping dictionary

# create visualization for çek renk
cek_color_df = visualization_df[['CEK_RENK']]
cek_color_df = cek_color_df['CEK_RENK'].value_counts()
# define a dictionary to map original labels to renamed çek renk labels
cek_renk_label_mapping = {'Ayesil': 'Açık Yeşil','Yesil':'Yeşil','Asari': 'Açık Sarı','Sari':'Sarı',
        'Turuncu':'Turuncu','Mor':'Mor','Kirmizi':'Kırmızı','Siyah':'Siyah'}
cek_color_df = cek_color_df.rename(index=cek_renk_label_mapping)     # rename the labels using the mapping dictionary
# reindex the labels in the desired order by using the list
cek_renk_order = ['Siyah', 'Kırmızı', 'Mor', 'Turuncu', 'Sarı', 'Açık Sarı', 'Yeşil', 'Açık Yeşil']
cek_color_df = cek_color_df.reindex(cek_renk_order)

# count number of MUSTERI and KESIDECI-> printing as metric with streamlit
customer_number = visualization_df[['MUSTERI_ID']]
customer_number = customer_number.drop_duplicates()     # customer_number.size

kesideci_number = visualization_df[['KESIDECI_ID']]
kesideci_number = kesideci_number.drop_duplicates()     # kesideci_number.size

cek_number = visualization_df[['CEK_NO']]
cek_number = cek_number.drop_duplicates()               # cek_number.size

# visualize "istihbarat sonucu"
# ...and make it a filter based on CEK_RENK
istihbarat_df=visualization_df[['CEK_NO','SIRKET_TURU','CEK_RENK','ISTIHBARAT_SONUC']]
istihbarat_df= istihbarat_df.drop_duplicates(subset='CEK_NO', keep="first")         # drop duplicates

# VISUALIZATIONS-RELATED TO BK TAB (Gerçek Kişiler TAB)
# query related attributes by filtering SIRKET_TURU as G (şahıs)
bk_query= """SELECT MUSTERI_ID, CEK_NO, BK_GECIKMEHESAP, CEK_TUTAR,
            BK_GECIKMEBAKIYE, BK_LIMIT, BK_RISK, BK_NOTU
            FROM dataset WHERE SIRKET_TURU LIKE 'G' """
visualization_bk_df = pd.read_sql(bk_query, cnxn)

sample_bk=visualization_bk_df.sample(n=1000)    # there is envy amount of data so using a sample
# scatter the limit by risk for G type customers
scatter_bklimitrisk = px.scatter(
    sample_bk[['BK_LIMIT','BK_RISK']],
    x="BK_LIMIT",
    y="BK_RISK",
)

# VISUALIZATIONS-RELATED TO TK TAB (Tüzel Kişiler TAB)
# query related attributes by filtering SIRKET_TURU as G (şahıs)
tk_query= """SELECT MUSTERI_ID, ID, CEK_NO, CEK_TUTAR, TK_NAKDILIMIT,
            TK_NAKDIRISK, TK_GAYRINAKDILIMIT, TK_GAYRINAKDIRISK, TK_GECIKMEHESAP, TK_GECIKMEBAKIYE
            FROM dataset WHERE SIRKET_TURU LIKE 'T' """
visualization_tk_df = pd.read_sql(tk_query, cnxn)

sample_tk=visualization_tk_df.sample(n=1000)    # there is envy amount of data so using a sample

# to see the number of occurrence of each customers for each customer type
bk_cektutar_df=visualization_bk_df[['CEK_NO', 'CEK_TUTAR', 'VADE_GUN']].drop_duplicates(subset='CEK_NO', keep="first")
tk_cektutar_df=visualization_tk_df[['CEK_NO', 'CEK_TUTAR', 'VADE_GUN']].drop_duplicates(subset='CEK_NO', keep="first")


# ----------------------------------------------
#   STARTING WEB-APP RELATED PARTS AFTER HERE
# ----------------------------------------------


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
col_up1.write(dummy_text)

# middle column
col_up2.subheader("Şahıs Şirketlerine Daha Sık Rastlıyoruz")
# this part stand for adjusting tooltip for donut chart
labels = companyType_df.index
values = companyType_df.values
hovertemplate_company = "%{label} kişilerde %{value} çek kaydı bulunmaktadır<extra></extra>"
figure_companyType = go.Figure(data=[go.Pie(labels=labels, values=values, hovertemplate=hovertemplate_company,
        hoverlabel=dict(align='left', font=dict(size=12)))])                              # create a donut chart
figure_companyType.update_traces(hole=0.4)                                                # set the hole size for the donut chart
figure_companyType.update_layout(legend=dict(orientation="h", yanchor="bottom",
                            y=1.02, xanchor="center", x=0.5))                             # adjust location of color legend for better visualization
col_up2.plotly_chart(figure_companyType, use_container_width=True)                        # render the chart for streamlit
# right column- metrices are declared here
col_up3.metric(label="Verisetindeki girdi sayısı", value=str(visualization_df['MUSTERI_ID'].size))
col_up3.metric(label="Verisetindeki müşteri sayısı", value=str(customer_number.size))
col_up3.metric(label="Verisetindeki keşideci sayısı", value=str(kesideci_number.size))
col_up3.metric(label="Verisetindeki çek sayısı", value=str(cek_number.size))
col_up3.write("Loren ipsum dolor sit amet. Loren ipsum dolor sit amet. Loren ipsum dolor sit amet.")

# create another column containers of web page
col_mid1,col_mid2=st.columns(2, gap="large")
col_mid1.subheader("Veri setindeki Çek Renkleri Sarı Ağırlıklı")
col_mid1.write(" Çek rengi KKB tarafından bankalara aktarılan bir bilgidir. Açık Yeşilden Siyaha sıralanmıştır. Açık Yeşil kredibilitesi en yüksek çektir, siyaha geçtikçe çekin kredibilitesi düşmektedir.")

cek_renk_color_palette=['#FFFFAD', '#FFFF99', '#FFFF85', '#FFFF70', '#FFFF5C', '#FFFF47', '#FFFF33', '#FFFF1F']
cek_color_fig = go.Figure(data=[go.Bar(x=cek_color_df,y=cek_color_df.index,orientation='h',
                    marker=dict(color=cek_renk_color_palette),
                    text=cek_color_df, textposition='auto', hoverinfo='none')])                         # creating the horizontal bar chart
cek_color_fig.update_layout(xaxis_title="Çek Miktarı",yaxis_title=None)                                 # set the chart axis labels
col_mid1.plotly_chart(cek_color_fig, use_container_width=True)                                         # render the chart for streamlit

col_mid2.write(dummy_text)
col_mid2.subheader("Çeklerin Şirket Türüne Göre İstihbarat Sonuçları")
# creating stacked bar chart for ISTIHBARAT_SONUC with respect to the company type
istihbarat_df_counts = istihbarat_df.groupby(['ISTIHBARAT_SONUC', 'SIRKET_TURU']).size().unstack().fillna(0)
colors_istihbaratChart = ['#FF4747', '#FF1F1F']         # defining custom colors for each category on the stacked bar chart
istihbarat_bar_chart = go.Figure(data=[
    go.Bar(name='Tüzel', x=istihbarat_df_counts.index, y=istihbarat_df_counts['T'], text=istihbarat_df_counts['T'],
                textposition='auto', marker=dict(color=colors_istihbaratChart[0]), hoverinfo='none'),
    go.Bar(name='Gerçek', x=istihbarat_df_counts.index, y=istihbarat_df_counts['G'], text=istihbarat_df_counts['G'],
                textposition='auto', marker=dict(color=colors_istihbaratChart[1]), hoverinfo='none')])
istihbarat_bar_chart.update_layout(barmode='stack',legend=dict(yanchor="bottom",y=1.02, xanchor="left", x=0.5))
col_mid2.plotly_chart(istihbarat_bar_chart, use_container_width=True)

col_down1,col_down2, col_down3 =st.columns(3, gap="large")
col_down1.write("Çek renklerinde kredibilitesi düşük çek renklerin ve ayrıca çek onlaylarında red durumundaki çek oranının yüksek olduğunu gözlemliyoruz.")
# oto-red ratio is calculated here
oto_red_count = istihbarat_df_counts.loc['RED']['T'] + istihbarat_df_counts.loc['RED']['G']
col_down1.metric(label="Oto Red Oranı", value=str(round(oto_red_count/cek_number.size*100, 2))+"%")
# siyah çek color count metric here
#black_cek_count = cek_color_df.loc['Siyah']
#col_down1.metric(label="Siyah Çek Oranı", value=str(round(black_cek_count/cek_number.size*100, 2))+"%")
col_down1.write("Bu durumun firma tarafından belirlenen müşteri risk seviyesiyle ne kadar örtüştüğünü görmek için yandaki grafikte müşterilerin risk seviyelerine göre dağılımını gözlemliyoruz.")

col_down2.subheader("Firma, Müşterilerini Çoğunlukla En Düşük Risk Seviyesinde Sınıflandırmış")
col_down2.bar_chart(riskLevel_df)                         # render the bar chart of risk level for streamlit

# creating tabs to navigate between charts of SIRKET_TURU T and G
tabT, tabG = st.tabs(["Tüzel Şirketler", "Şahıs Şirketleri"])
with tabT:
    st.header("Tüzel Şirketler")
    st.write('Tüzel şirketlerin hem nakdi hem de gayri nakdi limit ve risklerini gözlemliyoruz.Nakit halinde olmayan her türlü kredi, gayri nakdi olarak sınıflandırılır. Teminat mektubu, çek karnesi bu gruptadır. Gayri nakdi kredileryalnızca şirketlere sunulurken nakdi krediler şirketlere ve şahıslara sunulur.')
    # creating scatter plot for TK_NAKDILIMIT and TK_NAKDIRISK here
    scatter_trace = go.Scatter(x=sample_tk['TK_NAKDILIMIT'],y=sample_tk['TK_NAKDIRISK'],
    mode='markers',hovertemplate='Müşterinin Tüzel Nakdi Limiti %{x} ve Tüzel Nakdi Riski %{y} <extra></extra>')
    layout = go.Layout(xaxis_title="Kredi Limiti",yaxis_title="Kredi Riski")
    scatter_tk_nakdilimitrisk = go.Figure(data=scatter_trace, layout=layout)
    st.plotly_chart(scatter_tk_nakdilimitrisk, theme=None, use_container_width=True)

    st.write(dummy_text)   # dummy text for now

    # creating scatter plot for TK_GAYRINAKDILIMIT and TK_GAYRINAKDIRISK here
    scatter_trace = go.Scatter(x=sample_tk['TK_GAYRINAKDILIMIT'],y=sample_tk['TK_GAYRINAKDIRISK'],
    mode='markers',hovertemplate='Müşterinin Gayrinakdi Limiti %{x} ve Gayrinakdi Riski %{y} <extra></extra>')
    layout = go.Layout(xaxis_title="Kredi Limiti",yaxis_title="Kredi Riski")
    scatter_tk_nakdilimitrisk = go.Figure(data=scatter_trace, layout=layout)
    st.plotly_chart(scatter_tk_nakdilimitrisk, theme=None, use_container_width=True)

    st.bar_chart(tk_cektutar_df['VADE_GUN'].value_counts().sort_values(ascending=True), use_container_width=True)

with tabG:
    st.header("Şahıs Şirketleri")

    scatter_bklimitrisk.update_layout(xaxis=dict(showgrid=False, showticklabels=False))
    st.plotly_chart(scatter_bklimitrisk, theme=None, use_container_width=True)