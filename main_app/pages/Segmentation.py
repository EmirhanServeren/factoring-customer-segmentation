
# create a scatter plot for to describe the distribution of segments
tk_cluster_map = pd.read_feather('streamlit_view/tk_cluster_map.feather')
tk_cluster_map = tk_cluster_map.sample(1000)    # take sample for clear viz
# create a header before the chart
colup_T1.subheader("Outlier Customers Have Most Credit Risk")
colup_T1.write("It is possible to say T-Bronze is also kind of outlier as well. Because most of customers are included in reliable segment.")
# visualize the scatter plot
fig_tk_cluster_map = px.scatter(tk_cluster_map,
                        x="TOTAL_LIMIT", y="TOTAL_RISK",
                        color="CLUSTER_LABELS_3")
fig_tk_cluster_map.update_layout(xaxis_title='Credit Limit', yaxis_title='Credit Risk', legend_title='Segments')
#fig_tk_cluster_map.update_xaxes(range=[0, 1000000])      # edit axis range
#fig_tk_cluster_map.update_yaxes(range=[0, 1000000])      # edit axis range
# render the chart
colup_T1.plotly_chart(fig_tk_cluster_map, use_container_width=True)

# create a data frame for numeric distribution of segments
tk_cluster_distribution = pd.read_feather('streamlit_view/tk_cluster_distribution')
# give a context about chart in the head of next column container
colup_T2.markdown("""**T-Diamond is the most reliable segment.** T type mostly distributed in a single segment. **Due to their organizational structure.** """)
# print the numerical visualization right to the chart as a data frame
tk_cluster_distribution= tk_cluster_distribution.rename(columns={'Count':'Number of Customers'})
colup_T2.dataframe(tk_cluster_distribution.set_index('Segment'), use_container_width=True)
# give the remaining context under the data frame
colup_T2.markdown("""<p style='color: #FFFF00; font-style: bold; font-size: 18px;'>There were three cases on G type.
            There are two cases in T type.</p>""", unsafe_allow_html=True)
colup_T2.markdown("""<p style='color: #FF3333; font-style: bold; font-size: 18px;'>Low-rated offers are going to be presented for most of the T type customers. Because they are mostly reliable.</p>""", unsafe_allow_html=True)
colup_T2.markdown("""<p style='color: #FFFFFF; font-style: bold; font-size: 18px;'>Simply, the importance of division of T and G type customers are better presented with the segmentation model.</p>""", unsafe_allow_html=True)

# create a container for the next section
col_midT1, col_midT2 = st.columns(2)
# read data first, will be used over this section
cluster_results = pd.read_feather('streamlit_view/bk_tk_concat_cluster_result.feather')

# create a visualization that represents very often customer comparison between segments
col_midT1.subheader("Very Often Customers are Mostly in T type")
col_midT1.write("That makes sense why they are mostly segmented as reliable.")
# filter out outlier customers and T-Bronze
cluster_results = cluster_results[(cluster_results['Segment'] != 'outlier customers')]
cluster_results = cluster_results[(cluster_results['Segment'] != 'T-Bronze')]
# define colors for the bars
colors_veryOften_customers = ['lightblue' if segment == 'T-Diamond' else 'gray' for segment in cluster_results['Segment']]
# create the bar chart
fig_cluster_results_veryOften = go.Figure(data=[go.Bar(
        x=cluster_results['Segment'],y=cluster_results['Very Often'].sort_values(ascending=False),
        marker=dict(color=colors_veryOften_customers))])
fig_cluster_results_veryOften.update_traces(hovertemplate=None, hoverinfo='skip')
# render the chart
col_midT1.plotly_chart(fig_cluster_results_veryOften, use_container_width=True)




# reading the excel file "TAM FAKTORING PLAN"
#df = pd.read_excel('data/TAM FAKTÖRİNG PLAN.xlsx')
# display as a dataframe
#st.dataframe(df)