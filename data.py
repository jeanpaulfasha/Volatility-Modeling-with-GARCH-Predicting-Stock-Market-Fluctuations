"""This is for all the code used to interact with the AlphaVantage API and the SQLite database."""

import sqlite3
import pandas as pd
import requests
from config import settings

class AlphaVantageAPI:
    def __init__(self, api_key=settings.alpha_api_key):
    
        self.__api_key= api_key

    def get_daily(self, ticker, output_size="full"):

        # Create URL
        url = (
            "https://learn-api.wqu.edu/1/data-services/alpha-vantage/query?"
            "function=TIME_SERIES_DAILY&"
            f"symbol={ticker}&"
            f"outputsize={output_size}&"
            "datatype=json&"
            f"apikey={self.__api_key}"
        )

        # Send request to API
        response = requests.get(url)

        # Extract JSON data from response
        response_data = response.json()

        # Read data into DataFrame
        stock_data = response_data["Time Series (Daily)"]
        df = pd.DataFrame.from_dict(stock_data, orient="index", dtype=float)

        # Convert index to `DatetimeIndex` named "date"
        df.index = pd.to_datetime(df.index)
        df.index.name= "date"

        # Remove numbering from columns
        df.columns = [c.split(". ")[1] for c in df.columns]

        # Return DataFrame
        return df
    
class SQLRepository:
    def __init__(self, connection):
        self.connection = connection

    def insert_table(self, table_name, records, if_exists="fail"):
        n_inserted = records.to_sql(name=table_name, con=self.connection, if_exists=if_exists)
        return {
            "transaction_successful": True,
            "records_inserted": n_inserted
        }

    def read_table(self, table_name, limit=None):
        
        # Quote the table name to handle special characters like '.'
        table_name = f"'{table_name}'"

        # Build SQL query with optional limit
        query = f"SELECT * FROM {table_name}"
        if limit:
            query += f" LIMIT {limit}"

        # Read data into a DataFrame
        df = pd.read_sql(query, self.connection)

        # Ensure the "date" column is parsed as DatetimeIndex
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)

        # Ensure numeric columns are floats
        numeric_columns = ["open", "high", "low", "close", "volume"]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].astype(float)

        return df


