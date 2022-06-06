from logging import Logger
import os
from dataclasses import dataclass
import pandas as pd
import os
import pyodbc
import datetime as dt
import streamlit as st
import functools


@dataclass
class SQLEndpointInfo:
    host: str
    token: str
    http_path: str
    driver_path: str


class SQLEndpointRepository:
    """
    Base class for to data product
    """
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        endpoint_info = self.do_get_endpoint_info()
        self.connection = pyodbc.connect(
            self.do_get_connection_string(endpoint_info), autocommit=True
        )
        print('self.connection=' + 'good')

    @staticmethod
    def do_get_endpoint_info() -> SQLEndpointInfo:
        """
        This functions collects vital parameters required to build SQL Endpoint
        """
        for var in ["DBX_HOST", "DBX_TOKEN", "DBX_HTTP_PATH"]:
            if var not in os.environ:
                raise Exception(f"Environment variable {var} is not defined")

        host = os.environ["DBX_HOST"]
        token = os.environ["DBX_TOKEN"]
        http_path = os.environ["DBX_HTTP_PATH"]
        driver_path = os.environ.get(
            "SIMBA_DRIVER_PATH", "/opt/simba/spark/lib/64/libsparkodbc_sb64.so"
        )  # default location on Debian

        print('host=' + host)
        print('token=' + token)
        print('http_path=' + http_path)
        print('driver_path=' + driver_path)

        return SQLEndpointInfo(host, token, http_path, driver_path)

    @staticmethod
    def do_get_mapbox_token() -> str:
        """
        Getting access to MAPBOX via token
        """
        token = os.environ.get("MAPBOX_TOKEN")
        if not token:
            raise Exception(
                "Mapbox token missing, please create using URL:x https://studio.mapbox.com/"
            )
        return token

    @staticmethod
    def do_get_connection_string(endpoint_info: SQLEndpointInfo) -> str:
        """
        Bind connection parameters
        """
        connection_string = "".join(
            [
                f"DRIVER={endpoint_info.driver_path}",
                f";Host={endpoint_info.host}",
                ";PORT=443",
                f";HTTPPath={endpoint_info.http_path}",
                ";AuthMech=3",
                ";Schema=default",
                ";SSL=1",
                ";ThriftTransport=2",
                ";SparkServerType=3",
                ";UID=token",
                f";PWD={endpoint_info.token}",
                ";RowsFetchedPerBlock=100000",
            ]
        )
        return connection_string

    def do_get_data(self, query: str) -> pd.DataFrame:
        self.logger.debug(f"Running SQL query: {query}")
        start_time = dt.datetime.now()
        data = pd.read_sql(query, self.connection)
        end_time = dt.datetime.now()
        time_delta = end_time - start_time
        self.logger.debug(
            f"Query executed, returning the result. Total query time: {time_delta}"
        )
        return data


class TaxiSQLEndpointRepository(SQLEndpointRepository):
    def do_get_trips_by_minute(self, dt: dt.date) -> pd.DataFrame:
        query = f"""
        select 
            date_trunc('minute', pickup_datetime) as dt, 
            count(1) as amount_of_trips
        from default.nyctaxi_yellow
        where to_date(pickup_datetime) = "{dt}"
        group by 1
        order by 1
        """
        data = self.do_get_data(query)
        return data

    def do_get_raw_trips(self, date_filter_column: str, dt: dt.date) -> pd.DataFrame:
        query = f"""
        select 
            {date_filter_column},
            date_trunc('hour', pickup_datetime) as pickup_hour, 
            date_trunc('hour', dropoff_datetime) as dropoff_hour, 
            pickup_longitude,
            pickup_latitude,
            dropoff_longitude,
            dropoff_latitude,
            trip_distance
        from default.nyctaxi_yellow
        where 
            to_date({date_filter_column}) = "{dt}"
            and pickup_longitude is not null
            and pickup_latitude is not null
            and dropoff_longitude is not null
            and dropoff_latitude is not null
        """
        data = self.do_get_data(query)

        data["pickup_hour"] = pd.to_datetime(data["pickup_hour"]).dt.strftime("%H")
        data["dropoff_hour"] = pd.to_datetime(data["dropoff_hour"]).dt.strftime("%H")
        data.sort_values(by=date_filter_column, inplace=True)
        return data
