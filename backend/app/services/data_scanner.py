import duckdb
import pandas as pd


class DataScanner:

    @staticmethod
    def scan_csv(file_path: str) -> pd.DataFrame:

        query = f"""
        SELECT *
        FROM read_csv_auto('{file_path}')
        """

        dataframe = duckdb.query(query).to_df()

        return dataframe