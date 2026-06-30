import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
st.title("Sales Trend and Time-based Performance Dashboard")
df=pd.read_csv(r"C:\\Users\\lenovo\\Downloads\\Afficionado Coffee Roasters.csv")
df['revenue']=df['transaction_qty']*df['unit_price']
df["transaction_time"]=pd.to_datetime(df["transaction_time"],format="%H:%M:%S %p")
df["hour"]=df["transaction_time"].dt.hour
st.sidebar.header("Filters")
store=st.sidebar.selectbox("Select Store Location", df["store_location"].unique())
filtered_df=df[df["store_location"]==store]
#hour range slider
hour_range=st.sidebar.slider("Select Hour Range", 0, 23, (0,23))
filtered_df=filtered_df[(filtered_df["hour"]>=hour_range[0])& (filtered_df["hour"]<=hour_range[1])]
metric=st.sidebar.radio("Select Metric",["Revenue", "Quantity"])
st.subheader("Filtered Dataset Preview")
st.dataframe(filtered_df.head())
total_revenue=filtered_df["revenue"].sum()
total_transactions=filtered_df["transaction_id"].count()
peak_hour=filtered_df.groupby("hour")["revenue"].sum().idxmax()
col1,col2, col3=st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Transactions", total_transactions)
col3.metric("Peak Hour",f"{peak_hour}:00")
st.subheader("Hourly Revenue Distribution")
hourly_revenue=filtered_df.groupby("hour")["revenue"].sum()
st.bar_chart(hourly_revenue)
st.subheader("Hourly Transaction Volume")
hourly_transactions=filtered_df.groupby("hour")["transaction_qty"].sum()
st.bar_chart(hourly_transactions)
st.subheader("Revenue Heatmap by Store and Hour")
store_hour=df.pivot_table(values='revenue',index='store_location', columns='hour',aggfunc='sum')
fig, ax=plt.subplots(figsize=(10,4))
sns.heatmap(store_hour,cmap='coolwarm',annot=False,ax=ax)
st.pyplot(fig)
st.subheader("Revenue Comparision Across Store Loations")
location_revenue=df.groupby("store_location")["revenue"].sum()
st.bar_chart(location_revenue)
if metric=="Revenue":
       chart_data=filtered_df.groupby("hour")["revenue"].sum()
else:
        chart_data=filtered_df.groupby("hour")["transaction_qty"].sum()
st.bar_chart(chart_data)


