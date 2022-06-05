"""
Application entrypoint for streamlit. 
"""
import streamlit as st
import logging
import datetime as dt
from databricks_streamlit_demo.sql_endpoint_repository import TaxiSQLEndpointRepository
from databricks_streamlit_demo.ui_analytics import UIAnalytics
from databricks_streamlit_demo.helper import write_to_aligned_header, clear_date_warning


logger = logging.getLogger("databricks-streamlit-demo")
data_provider = TaxiSQLEndpointRepository(logger)
plotter = UIAnalytics(data_provider)

st.set_page_config(
    layout="wide", page_title="Data Product As Service", page_icon=":fire:" # :fire: will be transformed into emoji
)

st.write(
    """
# Data Product As Service using SQLEndpoint and analytics using Streamlit :fire:

This Streamlit application connects to Databricks SQL Endpoint and creates some analytics based on the [NYC Taxi Dataset](#https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page).
"""
)

clear_date_warning()

handle_filter_box, handle_minute_dynamic_box = st.beta_columns([1, 4])

with handle_filter_box:
    write_to_aligned_header("Please choose the date")
    chosen_date = st.date_input("", dt.date(2016, 6, 30))
    plotter.add_counter_plot(chosen_date)


with handle_minute_dynamic_box:
    plotter.add_minute_plot(chosen_date)

handle_pickups_map, handle_dropoffs_map = st.beta_columns(2)


with handle_pickups_map:
    plotter.add_density_map(chosen_date, name="pickup", zoom=11)

with handle_dropoffs_map:
    plotter.add_density_map(chosen_date, name="dropoff", zoom=9, alignment="right")
