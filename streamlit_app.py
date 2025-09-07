import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="Global Temperature Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

#######################
# Load data
df_temp = pd.read_csv('https://github.com/pennywa/temperature-dashboard/raw/main/combined_temperature.csv')
df_temp.columns = ['country', 'year', 'avg_temp', 'min_temp', 'max_temp']
df_temp['year'] = pd.to_datetime(df_temp['year'], format='%Y').dt.year

#######################
# Sidebar
with st.sidebar:
    st.title('🌍 Global Temperature Dashboard')
    
    # Select year range and country
    year_range = st.slider('Select Year Range', 1901, 2022, (1901, 2022))
    
    country_list = list(df_temp.country.unique())
    selected_country = st.selectbox('Select a country', country_list)

    # Filter data based on selections
    df_selected_year = df_temp[(df_temp['year'] >= year_range[0]) & (df_temp['year'] <= year_range[1])]
    
    df_selected_country = df_temp[df_temp.country == selected_country]


#######################
# Visualizations

# Line chart for selected country's temperature over time
st.markdown('#### Temperature Trend for ' + selected_country)
line_chart = alt.Chart(df_selected_country).mark_line().encode(
    x=alt.X('year:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15)),
    y=alt.Y('avg_temp:Q', axis=alt.Axis(title="Mean Temperature (°C)", titleFontSize=18, titlePadding=15)),
    tooltip=[
        alt.Tooltip('year:O', title='Year'),
        alt.Tooltip('avg_temp:Q', title='Mean Temp', format='.2f')
    ]
).properties(
    width=800,
    height=400
)

# Bar chart for comparing average temperatures of all countries for a selected year
st.markdown('#### Mean Temperature by Country (1901-2022)')
bar_chart = alt.Chart(df_selected_year).mark_bar().encode(
    x=alt.X('country:N', sort='-y', axis=alt.Axis(title="Country")),
    y=alt.Y('avg_temp:Q', axis=alt.Axis(title="Mean Temperature (°C)")),
    tooltip=[
        alt.Tooltip('country:N', title='Country'),
        alt.Tooltip('avg_temp:Q', title='Mean Temp', format='.2f')
    ]
).properties(
    width=800,
    height=400
)

# Choropleth map
st.markdown('#### Global Mean Temperature Map')
# To create the map, we need to get the average temperature per country for the selected year range
df_map = df_selected_year.groupby('country')['avg_temp'].mean().reset_index()

choropleth_map = px.choropleth(df_map, locations="country", color="avg_temp",
                    locationmode='country names',
                    hover_name="country",
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title="Global Mean Temperature",
                    labels={'avg_temp': 'Mean Temp (°C)'})

choropleth_map.update_layout(
    template='plotly_dark',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    margin=dict(l=0, r=0, t=0, b=0),
    height=500
)

#######################
# Dashboard Main Panel
st.title("Global Temperature Analysis (1901-2022)")
st.write("This dashboard visualizes mean temperatures for countries around the world based on data from 1901 to 2022.")

st.markdown("---")

# Display the charts
st.altair_chart(line_chart, use_container_width=True)
st.altair_chart(bar_chart, use_container_width=True)
st.plotly_chart(choropleth_map, use_container_width=True)
