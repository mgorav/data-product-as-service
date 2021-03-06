from typing import Optional
from plotly.missing_ipywidgets import FigureWidget
from data_product_service.sql_endpoint_repository import TaxiSQLEndpointRepository
import streamlit as st
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
from data_product_service.helper import (
    do_write_to_aligned_header,
    make_custom_spinner,
    clear_date_warning,
)

class UIAnalytics:
    def __init__(self, provider: TaxiSQLEndpointRepository) -> None:
        self.provider = provider
        px.set_mapbox_access_token(self.provider.do_get_mapbox_token())

    def add_counter_plot(self, chosen_date: dt.date) -> None:
        with make_custom_spinner("Loading total count ..."):
            cnt = self.provider.do_get_data(
                f"""
            select count(1) as cnt 
            from default.nyctaxi_yellow
            where to_date(pickup_datetime) = "{chosen_date}"
            """
            ).loc[0, "cnt"]
            fig = go.Figure(
                go.Indicator(
                    mode="number",
                    value=cnt,
                    align="center",
                    title={"text": "Total pickups"},
                )
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    def add_minute_plot(self, chosen_date: dt.date) -> None:
        do_write_to_aligned_header("Number of trips per minute", alignment="right")
        with make_custom_spinner("Loading minute plot ..."):
            data = self.provider.do_get_trips_by_minute(chosen_date)
            fig = px.area(
                data,
                x="dt",
                y="amount_of_trips",
                labels={"dt": "time", "amount_of_trips": "Number of Trips"},
                height=500,
            )
            st.plotly_chart(fig, use_container_width=True)

    def _get_density_map(
        self,
        chosen_date: dt.date,
        date_filter_column: str,
        lat_col: str,
        lon_col: str,
        frame_col: str,
        zoom: int = 10,
    ) -> Optional[FigureWidget]:
        data = self.provider.do_get_raw_trips(date_filter_column, chosen_date)
        if data.empty:
            return None
        else:
            fig = px.density_mapbox(
                data_frame=data,
                lat=lat_col,
                lon=lon_col,
                zoom=zoom,
                z="trip_distance",
                radius=10,
                opacity=0.7,
                mapbox_style="dark",
                animation_frame=frame_col,
                center={"lat": 40.7359, "lon": -73.9911},  # NY Central Park Coordinates
                height=600,
                labels={"pickup_hour": "Pickup Hour", "dropoff_hour": "Dropoff Hour"},
            )
            return fig

    def add_density_map(
        self,
        chosen_date: dt.date,
        name: str,
        alignment: Optional[str] = None,
        zoom: Optional[int] = 10,
    ) -> None:
        do_write_to_aligned_header(f"{name.capitalize()} density map", alignment=alignment)

        with make_custom_spinner(f"Loading {name} density map ..."):
            fig = self._get_density_map(
                chosen_date,
                f"{name}_datetime",
                f"{name}_latitude",
                f"{name}_longitude",
                f"{name}_hour",
                zoom=zoom,
            )
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                clear_date_warning()
