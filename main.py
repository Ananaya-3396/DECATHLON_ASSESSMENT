import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform

data = pd.read_csv("Decathlon_clean_data.csv")

del data["Unnamed 0"]


def main():

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to",
                                ["Whole Data", "Filtered Data", "Country Wise Analysis Report", "Customer Analytics Report"])

    if page == "Whole Data":
        whole_data(data)
    elif page == "Filtered Data":
        filtered_data_function(filtered_data)
    elif page == "Country Wise Analysis Report":
        country_analysis_function(filtered_data)
    elif page == "Customer Analytics Report":
        cust_analytics_function(filtered_data)




def whole_data(data):
    if st.sidebar.button('View Data'):
        st.title('Customer Transaction Data')
        st.write(data, )



country = st.sidebar.multiselect("Select the country you want to look",
                                   options=data["Country"].unique(),

                                   )
filtered_data = data[data["Country"].isin(country)]




def country_analysis_function(filtered_data):
# Plot vehicle age vs km driven using bar chart
    if not filtered_data.empty:
        chart_data1 = filtered_data.groupby(["Country"])[["Total_Price"]].sum().sort_values(by = "Total_Price", ascending = False).reset_index()
        bar_chart1 = alt.Chart(chart_data1).mark_bar().encode(
            x='Country:O',
            y='Total_Price:Q'
        ).properties(
            width=600,
            height=400)


        st.write("Country vs Total Spend")
        st.altair_chart(bar_chart1, use_container_width=True)

    if not filtered_data.empty:
        chart_data2 = filtered_data.groupby(["Country"])[["Customer ID"]].count().reset_index().rename(columns = {"Customer ID": "Customer Count"}).sort_values(by = "Customer Count", ascending = False)
        bar_chart2 = alt.Chart(chart_data2).mark_bar().encode(
            x='Country:O',
            y='Customer Count:Q'
        ).properties(
            width=600,
            height=400)


        st.write("Country vs Customer Count")
        st.altair_chart(bar_chart2, use_container_width=True)


def cust_analytics_function(filtered_data):


    metric_options = ['Total_Price', 'Invoice']
    selected_metric = st.sidebar.selectbox("Select the metric for customer analytics report", metric_options)


    if not filtered_data.empty:
        if selected_metric == "Total_Price":
            chart_data3 = filtered_data.groupby(['Country',"Customer ID"])[["Total_Price"]].sum().reset_index()
            bar_chart3 = alt.Chart(chart_data3).mark_bar().encode(
                x='Customer ID:O',
                y='Total_Price:Q',
                color='Country:N'
            ).properties(
                width=600,
                height=400)

            st.write("Customer Spending amount")
            st.altair_chart(bar_chart3, use_container_width=True)
        else:
            chart_data3 = filtered_data.groupby(['Country',"Customer ID"])[["Invoice"]].nunique().reset_index()
            bar_chart3 = alt.Chart(chart_data3).mark_bar().encode(
                x='Customer ID:O',
                y='Invoice:Q',
                color='Country:N'
            ).properties(
                width=600,
                height=400)

            st.write("Customer Invoice Count")
            st.altair_chart(bar_chart3, use_container_width=True)






def filtered_data_function(filtered_data):
    if st.sidebar.button('View Filtered Data'):
        st.title('Filtered Data')
        st.write(filtered_data, height=800)


if __name__ == "__main__":
    main()
