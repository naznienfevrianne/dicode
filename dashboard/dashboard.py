# Nama          : Naznien Fevrianne Malano                      
# Email         : m010d4kx1713@bangkit.academy                  
# Id Dicoding   : m010d4kx1713                                  
# Github Pages  : naznienfevrianne.github.io                    
# Created       : 3 Maret 2024                                  

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

@st.cache_resource
def load_data():
    data = pd.read_csv("../data/hour.csv")
    return data

def load_data_day():
    data = pd.read_csv("../data/day.csv")
    return data

def create_heatmap(data):
    plt.figure(figsize=(10, 10))
    sns.heatmap(data.select_dtypes(np.number).corr(method='spearman'),
                annot=True,
                cbar=False,
                fmt="0.2f",
                cmap="YlGnBu",
                xticklabels=data.select_dtypes(np.number).columns,
                yticklabels=data.select_dtypes(np.number).columns)
    plt.title("Correlation matrix")
    return plt


data = load_data()
data_day = load_data_day()

st.title("Bike Share Dashboard :sparkles:")
st.markdown("Author: \n Naznien Fevrianne Malano")
st.markdown("Contact me through: \n [Linkedin](https://www.linkedin.com/in/naznien-fevrianne-malano-3b59a4190/)  [GitHub Pages](https://naznienfevrianne.github.io/)")

# Show the dataset
st.subheader("Raw data of hour.csv")
st.write(data)
st.subheader("Raw data of day.csv")
st.write(data_day)

    
st.subheader("Statistic descriptive of hour.csv")
st.write(data.describe())
st.subheader("Statistic descriptive of day.csv")
st.write(data_day.describe())

st.subheader("Daily rents")
total_rental = data_day["cnt"].sum()
st.write("Total rents (1st January 2011 - 31st December 2012): " + str(total_rental))
daily_count = data.groupby("dteday")['cnt'].sum().reset_index(name="rental_count")
fig_daily_count = px.line(
    daily_count, x="dteday", y="rental_count", title="Daily Bike Share Trend")
st.plotly_chart(fig_daily_count, use_container_width=True,
                height=400, width=600)


st.subheader("Comparing data from day with lowest and highest rental")
data_day['dteday'] = pd.to_datetime(data_day['dteday'])
# Find the instant value for the day with the highest rental count
instant_highest_rentals = data_day.loc[data_day['cnt'].idxmax(), 'instant']
# Find the instant value for the day with the lowest rental count
instant_lowest_rentals = data_day.loc[data_day['cnt'].idxmin(), 'instant']
comparison_df = data_day.loc[(data_day['instant'] == instant_highest_rentals) | (data_day['instant'] == instant_lowest_rentals) ]
st.write(comparison_df)

weather_mapping = {1: "Sunny", 2: "Cloudy", 3:"Light Rain/Snow", 4: "Heavy Rain/Snow"}
data["weather_label"] = data["weathersit"].map(weather_mapping)

st.subheader("Comparing Mean of Rentals in Every Season and Weather Situation")
weather_count = data.groupby("weather_label")["cnt"].sum().reset_index()
fig_weather_count = px.bar(weather_count, x="weather_label",
                            y="cnt", title="Rental Counts by Weather Situation")

season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
data["season_label"] = data["season"].map(season_mapping)

st.plotly_chart(fig_weather_count, use_container_width=True,height=300, width=700)
season_count = data.groupby("season_label")["cnt"].sum().reset_index()
fig_season_count = px.bar(season_count, x="season_label",
                            y="cnt", title="Rental Counts by Season")

st.plotly_chart(fig_season_count, use_container_width=True,height=300, width=700)

st.subheader("Rental trends over hour")

# Hourly bike share count
# st.subheader("Hourly Bike Share Count")
hourly_count = data.groupby("hr")["cnt"].sum().reset_index()
fig_hourly_count = px.line(
    hourly_count, x="hr", y="cnt", title="Hourly Bike Share Trend")
st.plotly_chart(fig_hourly_count, use_container_width=True,
                height=400, width=600)

st.subheader("Casual and Registered User Trends")


data['dteday'] = pd.to_datetime(data['dteday'])

# Group by 'dteday' and sum the 'casual' and 'registered' counts
user_counts_over_time = data.groupby('dteday')[['casual', 'registered']].sum().reset_index()

# Create a line plot
fig_user_counts = px.line(user_counts_over_time, x='dteday', y=['casual', 'registered'],
                          labels={'value': 'Count', 'variable': 'User Type'},
                          title='Casual and Registered User Counts Over Time')
st.plotly_chart(fig_user_counts, use_container_width=True,
                height=400, width=600)

st.subheader("The rental count vary during days")

# Assuming data_day is your DataFrame with a datetime column (e.g., 'dteday')
# Make sure 'dteday' is in datetime format
data_day['dteday'] = pd.to_datetime(data_day['dteday'])

# Extract the day of the week from 'dteday'
data_day['day_of_week'] = data_day['dteday'].dt.day_name()

# Group by 'day_of_week' and calculate the average 'cnt' for each day
average_cnt_by_day = data_day.groupby('day_of_week')['cnt'].mean().reset_index()

# Create a bar chart
fig_average_cnt_by_day = px.bar(average_cnt_by_day, x='day_of_week', y='cnt',
                                labels={'cnt': 'Average Count', 'day_of_week': 'Day of Week'},
                                title='Average Count of Bikes Rented by Day of Week')
st.plotly_chart(fig_average_cnt_by_day, use_container_width=True,
                height=400, width=600)


# Show data source and description
st.sidebar.title("Dataset characteristics")
st.sidebar.info("""Both hour.csv and day.csv have the following fields, except hr which is not available in day.csv
	
	- instant: record index
	- dteday : date
	- season : season 
      - 1:spring, 
      - 2:summer,
      - 3:fall, 
      - 4:winter)
	- yr : year (0: 2011, 
      1:2012)
	- mnth : month ( 1 to 12)
	- hr : hour (0 to 23)
	- holiday : day is holiday 
      or not 
	- weekday : day of the 
      week
	- workingday : day is 
      working day or not
	+ weathersit : 
	  - 1: Sunny
	  - 2: Cloudy
	  - 3: Light Snow/Rain
	  - 4: Heavy Snow/Rain
	- temp : Normalized 
      temperature in Celsius. 
	- atemp: Normalized 
      feeling temperature 
      in Celsius. 
	- hum: Normalized 
      humidity. 
	- windspeed: Normalized
      wind speed. 
	- casual: count of casual 
      users
	- registered: count of 
      registered users
	- cnt: count of total 
      rental bikes" """)

