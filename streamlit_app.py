#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="Average Temperature of Countries from 1901 - 2022",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
