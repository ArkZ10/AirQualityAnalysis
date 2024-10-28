import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_csv("Dashboard/main_data.csv")

data['datetime'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])

st.sidebar.header("Select Date Range")
start_date = st.sidebar.date_input("Start Date", min_value=data['datetime'].min(), max_value=data['datetime'].max(), value=data['datetime'].min())
end_date = st.sidebar.date_input("End Date", min_value=data['datetime'].min(), max_value=data['datetime'].max(), value=data['datetime'].max())

data_filtered = data[(data['datetime'] >= pd.to_datetime(start_date)) & (data['datetime'] <= pd.to_datetime(end_date))]

st.sidebar.header("Visualization Options")
column_options = ["PM2.5", "PM10", "TEMP", "DEWP", "WSPM"]  # Adjust based on available columns
selected_column = st.sidebar.selectbox("Select Column to Visualize", column_options)

location_options = ["Shunyi", "Guanyan"]
selected_location = st.sidebar.selectbox("Select Location", location_options)

column_name = f"{selected_column}_{selected_location.lower()}"

st.write(f"Data from {start_date} to {end_date}")
st.dataframe(data_filtered)

st.header(f"{selected_column} Levels at {selected_location}")

fig, ax = plt.subplots()
ax.plot(data_filtered["datetime"], data_filtered[column_name], label=f"{selected_column} ({selected_location})")
ax.set_xlabel("Date and Time")
ax.set_ylabel(f"{selected_column} Levels")
ax.legend()

plt.gcf().autofmt_xdate()

st.pyplot(fig)

st.header("Correlation Heatmap")

heatmap_columns = [f"{col}_{selected_location.lower()}" for col in column_options]
data_corr = data_filtered[heatmap_columns].corr()

fig, ax = plt.subplots()
sns.heatmap(data_corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
ax.set_title(f"Correlation Heatmap for {', '.join(column_options)} in {selected_location}")
st.pyplot(fig)

pm2_5_bins_shunyi = [
    data_filtered['PM2.5_shunyi'].min(),
    data_filtered['PM2.5_shunyi'].quantile(0.25),
    data_filtered['PM2.5_shunyi'].quantile(0.5),
    data_filtered['PM2.5_shunyi'].quantile(0.75),
    data_filtered['PM2.5_shunyi'].max()
]

pm10_bins_shunyi = [
    data_filtered['PM10_shunyi'].min(),
    data_filtered['PM10_shunyi'].quantile(0.25),
    data_filtered['PM10_shunyi'].quantile(0.5),
    data_filtered['PM10_shunyi'].quantile(0.75),
    data_filtered['PM10_shunyi'].max()
]

pm2_5_bins_guanyan = [
    data_filtered['PM2.5_guanyan'].min(),
    data_filtered['PM2.5_guanyan'].quantile(0.25),
    data_filtered['PM2.5_guanyan'].quantile(0.5),
    data_filtered['PM2.5_guanyan'].quantile(0.75),
    data_filtered['PM2.5_guanyan'].max()
]

pm10_bins_guanyan = [
    data_filtered['PM10_guanyan'].min(),
    data_filtered['PM10_guanyan'].quantile(0.25),
    data_filtered['PM10_guanyan'].quantile(0.5),
    data_filtered['PM10_guanyan'].quantile(0.75),
    data_filtered['PM10_guanyan'].max()
]

# Labels for the bins
labels = ['Low', 'Medium', 'High', 'Very High']

data_filtered['PM2.5_Percentile_Category_shunyi'] = pd.cut(data_filtered['PM2.5_shunyi'], bins=pm2_5_bins_shunyi, labels=labels, include_lowest=True)
data_filtered['PM10_Percentile_Category_shunyi'] = pd.cut(data_filtered['PM10_shunyi'], bins=pm10_bins_shunyi, labels=labels, include_lowest=True)

data_filtered['PM2.5_Percentile_Category_guanyan'] = pd.cut(data_filtered['PM2.5_guanyan'], bins=pm2_5_bins_guanyan, labels=labels, include_lowest=True)
data_filtered['PM10_Percentile_Category_guanyan'] = pd.cut(data_filtered['PM10_guanyan'], bins=pm10_bins_guanyan, labels=labels, include_lowest=True)

color_map = {
    'Low': 'green',
    'Medium': 'yellow',
    'High': 'orange',
    'Very High': 'red'
}

st.header("Scatter Plot of PM2.5 vs PM10 with Percentile Bins (Shunyi)")
fig_shunyi = go.Figure()

for category in labels:
    subset = data_filtered[data_filtered['PM2.5_Percentile_Category_shunyi'] == category]
    fig_shunyi.add_trace(go.Scatter3d(
        x=subset['PM2.5_shunyi'],
        y=subset['PM10_shunyi'],
        z=subset['TEMP_shunyi'],
        mode='markers',
        marker=dict(size=5, color=color_map[category]),
        name=f'PM2.5 {category}'
    ))

fig_shunyi.update_layout(scene=dict(
    xaxis_title='PM2.5 Concentration (Shunyi)',
    yaxis_title='PM10 Concentration (Shunyi)',
    zaxis_title='Temperature (Shunyi)'
), title="Scatter Plot of PM2.5 vs PM10 with Temperature (Shunyi)")

st.plotly_chart(fig_shunyi)

st.header("Scatter Plot of PM2.5 vs PM10 with Percentile Bins (Guanyan)")
fig_guanyan = go.Figure()

for category in labels:
    subset = data_filtered[data_filtered['PM2.5_Percentile_Category_guanyan'] == category]
    fig_guanyan.add_trace(go.Scatter3d(
        x=subset['PM2.5_guanyan'],
        y=subset['PM10_guanyan'],
        z=subset['TEMP_guanyan'],
        mode='markers',
        marker=dict(size=5, color=color_map[category]),
        name=f'PM2.5 {category}'
    ))

fig_guanyan.update_layout(scene=dict(
    xaxis_title='PM2.5 Concentration (Guanyan)',
    yaxis_title='PM10 Concentration (Guanyan)',
    zaxis_title='Temperature (Guanyan)'
), title="Scatter Plot of PM2.5 vs PM10 with Temperature (Guanyan)")

st.plotly_chart(fig_guanyan)

