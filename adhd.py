import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Set page title
st.set_page_config(page_title='ADHD Student Dashboard', layout='wide')

# Title
st.title('ADHD Student Performance Dashboard')

# Generate sample data
np.random.seed(42)
start_date = datetime.today() - timedelta(days=365)
dates = [start_date + timedelta(days=i) for i in range(365)]

# Sample data generation
data = {
    'Date': dates,
    'Activeness': np.random.randint(0, 100, size=365),
    'Time Spent (min)': np.random.randint(10, 120, size=365),
    'Active Concentration (%)': np.random.randint(0, 100, size=365),
    'Comprehension Score (%)': np.random.randint(0, 100, size=365),
    'Break Frequency': np.random.randint(0, 10, size=365),
    'Hyperactivity Incidents': np.random.randint(0, 15, size=365),
    'Distraction Frequency': np.random.randint(0, 50, size=365),
    'Task Completion (%)': np.random.randint(0, 100, size=365)
}

df = pd.DataFrame(data)

# Normalization of activeness data
df['Normalized Activeness'] = df['Activeness'] / df['Activeness'].max()

# Display key performance metrics on top
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
col1.metric('Avg Activeness (%)', f"{df['Activeness'].mean():.2f}")
col2.metric('Avg Comprehension (%)', f"{df['Comprehension Score (%)'].mean():.2f}")
col3.metric('Max Activeness (%)', f"{df['Activeness'].max()}%")
col4.metric('Total Time Spent (hrs)', f"{df['Time Spent (min)'].sum() / 60:.2f}")
col5.metric('Avg Break Frequency', f"{df['Break Frequency'].mean():.2f}")
col6.metric('Avg Hyperactivity Incidents', f"{df['Hyperactivity Incidents'].mean():.2f}")
col7.metric('Avg Distraction Frequency', f"{df['Distraction Frequency'].mean():.2f}")
col8.metric('Avg Task Completion (%)', f"{df['Task Completion (%)'].mean():.2f}")

# Activity Level Over Time
df['Week'] = df['Date'].dt.isocalendar().week
df['Day'] = df['Date'].dt.weekday

# Aggregate duplicate 'Day' and 'Week' combinations by taking the mean
df_agg = df.groupby(['Day', 'Week'])['Normalized Activeness'].mean().reset_index()

# Pivot the aggregated data
heatmap_data = df_agg.pivot(index='Day', columns='Week', values='Normalized Activeness')

fig = go.Figure(data=go.Heatmap(
    z=heatmap_data,
    x=heatmap_data.columns,
    y=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    colorscale='Greens',
    showscale=True,
    zmin=0, zmax=1
))

fig.update_layout(
    title='Activity Level Over Time (Darker Green = More Active)',
    xaxis_nticks=52,
    yaxis_nticks=7,
    xaxis_title='Week',
    yaxis_title='Day of the Week'
)

st.plotly_chart(fig, use_container_width=True)

# Date range selection for line charts
selected_range = st.date_input('Select Date Range', [dates[0], dates[29]])
filtered_df = df[(df['Date'] >= pd.to_datetime(selected_range[0])) & (df['Date'] <= pd.to_datetime(selected_range[1]))]

# Time spent and active concentration line chart
fig1 = px.line(filtered_df, x='Date', y=['Time Spent (min)', 'Active Concentration (%)'],
               title='Time Spent & Active Concentration Over Time', markers=True,
               labels={'value': 'Minutes / %', 'Date': 'Date'},
               line_shape='linear')
st.plotly_chart(fig1, use_container_width=True)

# Comprehension score line chart with custom markers
fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=filtered_df['Date'],
    y=filtered_df['Comprehension Score (%)'],
    mode='lines+markers',
    line=dict(color='blue'),
    marker=dict(
        size=[14 if val > 85 else 8 for val in filtered_df['Comprehension Score (%)']],
        symbol=['star' if val > 85 else 'circle' for val in filtered_df['Comprehension Score (%)']],
        color=['yellow' if val > 85 else 'blue' for val in filtered_df['Comprehension Score (%)']],
        line=dict(color='black', width=1)
    )
))
fig2.update_layout(title='Comprehension Score Over Time',
                   xaxis_title='Date',
                   yaxis_title='Comprehension Score (%)')

st.plotly_chart(fig2, use_container_width=True)

# Break frequency and hyperactivity incidents line chart
fig3 = px.line(filtered_df, x='Date', y=['Break Frequency', 'Hyperactivity Incidents'],
               title='Break Frequency & Hyperactivity Incidents Over Time', markers=True,
               labels={'value': 'Frequency', 'Date': 'Date'},
               line_shape='linear')
st.plotly_chart(fig3, use_container_width=True)

# Distraction frequency line chart
fig4 = px.line(filtered_df, x='Date', y='Distraction Frequency',
               title='Distraction Frequency Over Time', markers=True,
               labels={'value': 'Frequency', 'Date': 'Date'},
               line_shape='linear')
st.plotly_chart(fig4, use_container_width=True)

