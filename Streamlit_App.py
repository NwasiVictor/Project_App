import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import date

# Load dataset
df = pd.read_csv("victor.csv")
df['Start date'] = pd.to_datetime(df['Start date'])
df['End date'] = pd.to_datetime(df['End date'])
df['Duration'] = (df['End date'] - df['Start date']).dt.days
df['Year'] = df['Start date'].dt.year
df['Month'] = df['Start date'].dt.month

# User profile
st.sidebar.title("User Profile")
st.sidebar.write("Nwasi Victor Obinna")
st.sidebar.write("Data Analyst")

st.sidebar.divider()

# Filters
st.sidebar.header("filters")

# State selection
states = st.sidebar.multiselect(
    "Select State(s)",
    options=sorted(df["State"].dropna().unique())
)

# Start date
start_date = st.sidebar.date_input("Start Date", value=df['Start date'].min().date())

# End date
end_date = st.sidebar.date_input("End Date", value=df['End date'].max().date())

# Apply filters
mask = (df['Start date'].dt.date >= start_date) & (df['End date'].dt.date <= end_date)
if states:
    mask &= df['State'].isin(states)

filtered_df = df[mask]

st.title("Incident Analysis Dashboard")

# Q1: How have incidents changed over the years?
st.subheader("1. How have incidents changed over the years?")
incidents_per_year = filtered_df.groupby('Year').size().reset_index(name='count')
fig1 = px.line(incidents_per_year, x='Year', y='count', markers=True,
               color_discrete_sequence=px.colors.qualitative.Set2,
               title="Incidents per Year")
st.plotly_chart(fig1, use_container_width=True)

st.info("""
Insight:Nigeria recorded over 169,000 violent deaths between 2006 and 2021,
with a peak in 2014 (22,873 deaths) largely due to Boko Haram insurgency in the North-East.
More recent FRSC data shows road crashes killed 10,081 people between 2023–2024,
with fatalities rising even as crash numbers fell.""")

# Q2: Which states recorded the most fatalities?
st.subheader("2. Which states recorded the most fatalities?")
deaths_by_state = filtered_df.groupby('State')['Number of deaths'].sum().reset_index().sort_values('Number of deaths', ascending=False)
fig2 = px.bar(deaths_by_state, x='Number of deaths', y='State', orientation='h',
              color='Number of deaths', color_continuous_scale='Reds',
              title="Total Deaths by State")
st.plotly_chart(fig2, use_container_width=True)

st.info("""Insight:Borno State consistently tops fatality counts, followed by Zamfara, Kaduna, Niger, Plateau,
and Benue. In Q1 2024 alone, Zamfara (439 deaths) and Borno (437 deaths) were the most affected,
while Gombe and Kano reported almost no deaths.""")


# Q3: Which states had the highest incident frequency?
st.subheader("3. Which states had the highest incident frequency?")
fig3 = alt.Chart(filtered_df).mark_bar().encode(
    x='State',
    y='count()',
    tooltip=['State','count()']
).properties(title='Incident Frequency by State')
st.altair_chart(fig3, use_container_width=True)

st.info("""
Insight:Incident frequency is highest in Bauchi, Borno, and Benue, according to Nigeria’s Risk Index.
These states report frequent attacks, kidnappings, and communal clashes, even when fatalities are lower than in Zamfara or Kaduna.
""")

# Q4: Do incidents cluster in certain months?
st.subheader("4. Do incidents cluster in certain months?")
incidents_per_month = filtered_df.groupby('Month').size().reset_index(name='count')
fig4 = px.line(incidents_per_month, x='Month', y='count', markers=True,
               color_discrete_sequence=px.colors.qualitative.Bold,
               title="Incidents per Month")
st.plotly_chart(fig4, use_container_width=True)

st.info("""
Insight:Nigeria’s rainy season (April–October) coincides with higher incidents, especially in rural areas where farming 
activities increase exposure to banditry and herder clashes. Fatalities from pastoral conflicts often peak in
 August–September, while road crashes spike during December festive travel.""")

# Q5: Which incident types are most deadly?
st.subheader("5. Which incident types are most deadly?")
avg_deaths_by_incident = filtered_df.groupby('Incident')['Number of deaths'].mean().reset_index()
fig5 = px.bar(avg_deaths_by_incident, x='Incident', y='Number of deaths',
              color='Number of deaths', color_continuous_scale='Viridis',
              title="Average Deaths per Incident Type")
st.plotly_chart(fig5, use_container_width=True)

st.info("""
Insight: The deadliest incident types are crime-related killings (51,425 deaths), insurgency (50,252 deaths), 
and road crashes (27,645 deaths) between 2006 – 2021.In 2023, rural banditry, Boko Haram attacks, and farmer–herder 
clashes were leading causes of fatalities.""")

# Q6: Has the severity of incidents increased or decreased?
st.subheader("6. Has the severity of incidents increased or decreased?")
avg_deaths_per_year = filtered_df.groupby('Year')['Number of deaths'].mean().reset_index()
fig6 = px.line(avg_deaths_per_year, x='Year', y='Number of deaths', markers=True,
               color_discrete_sequence=px.colors.qualitative.Dark2,
               title="Average Deaths per Year")
st.plotly_chart(fig6, use_container_width=True)

st.info("""
Insight: Severity has increased. For example, in 2024, Nigeria recorded fewer crashes (9,570 vs 10,617 in 2023) 
but more deaths (5,421 vs 5,081). Similarly, terrorism-related deaths rose by 6% in 2024, even though attacks declined by
37%. This shows incidents are becoming deadlier per occurrence.""")

# Q7: Top 10 deadliest incidents
st.subheader("7. Top 10 deadliest incidents")
top10 = filtered_df.nlargest(10, 'Number of deaths')[['Identifier','Incident','State','Number of deaths']]
fig7 = px.bar(top10, x='Incident', y='Number of deaths',
              color='State', title="Top 10 Deadliest Incidents")
st.plotly_chart(fig7, use_container_width=True)
st.dataframe(top10)

st.info("""
Insight:Nigeria’s deadliest recent incidents include Boko Haram and ISWAP attacks in Yobe and Borno (2024–2025), 
killing up to 100 people in a single assault. In Benue (2025), the Yelewata and Daudu massacre killed at least 59–200 people,
 making it one of the worst communal clashes in recent history.""")
