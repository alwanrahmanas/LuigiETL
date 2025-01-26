import requests
import luigi
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv("Week 8/.env")

def data_json(url):
    """
    Fetch JSON data from a URL and return it as a Python dictionary.

    Parameters:
        url (str): The URL to fetch JSON data from.

    Returns:
        dict or str: The JSON data as a dictionary if successful, otherwise an error message.
    """
    try:
        print(f"Fetching data from URL: {url}")
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Request successful. Parsing JSON data...")
            data = response.json()  # Automatically parses JSON into a Python dictionary
            return data  # Return the JSON data
        else:
            error_msg = f"Failed to fetch JSON. HTTP Status Code: {response.status_code}"
            print(error_msg)
            return error_msg
    
    except requests.exceptions.RequestException as e:
        error_msg = f"An error occurred: {e}"
        print(error_msg)
        return error_msg

def postgres_engine():
    """
    Create and return a SQLAlchemy engine for a PostgreSQL database.

    Returns:
        Optional[create_engine]: A SQLAlchemy engine object, or None if an error occurs.
    """
    print("Creating PostgreSQL engine...")
    # Fetch environment variables
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    # Debug: Print the retrieved values
    print(f"DB_USER: {db_user}")
    print(f"DB_PASSWORD: {db_password}")
    print(f"DB_HOST: {db_host}")
    print(f"DB_PORT: {db_port}")
    print(f"DB_NAME: {db_name}")

    # Check if all required environment variables are set
    if not all([db_user, db_password, db_host, db_port, db_name]):
        error_msg = "One or more required environment variables are not set."
        print(error_msg)
        raise ValueError(error_msg)

    # Create the database URL
    database_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    # Create and return the engine
    engine = create_engine(database_url)
    print("PostgreSQL engine created successfully.")
    return engine

def read_sql(table_name: str):
    """
    Query a PostgreSQL table and return the results as a DataFrame.

    Parameters:
        table_name (str): The name of the table to query.

    Returns:
        pd.DataFrame: The query results as a DataFrame.
    """
    print(f"Querying table: {table_name}")
    engine = postgres_engine()
    query = f"SELECT * FROM public.{table_name};"
    df = pd.read_sql(query, engine)
    print(f"Retrieved {len(df)} rows from table '{table_name}'.")
    return df

class ExtractFromJson(luigi.Task):
    """
    Luigi task to extract data from a JSON API and save it to a CSV file.
    """
    url = luigi.Parameter(default="https://shandytepe.github.io/payment.json")  # Example JSON API URL

    def output(self):
        return luigi.LocalTarget("df.csv")

    def run(self):
        print("Starting ExtractFromJson task...")
        # Fetch JSON data
        json_data = data_json(self.url)

        if isinstance(json_data, dict):
            print("JSON data fetched successfully. Converting to DataFrame...")
            # Convert JSON data to DataFrame
            raw_data = json_data['payment_data']
            df = pd.DataFrame(raw_data)

            # Save DataFrame to CSV
            df.to_csv(self.output().path, index=False)
            print(f"Data saved to {self.output().path}")
        else:
            error_msg = f"Failed to fetch JSON data: {json_data}"
            print(error_msg)
            raise ValueError(error_msg)

class ExtractFromDB(luigi.Task):
    """
    Luigi task to extract data from multiple PostgreSQL tables and save them to separate CSV files.
    """
    table_names = luigi.ListParameter(default=["reservation", "customer"])  # List of table names

    def output(self):
        # Create a list of output targets (one CSV file per table)
        return [luigi.LocalTarget(f"{table_name}.csv") for table_name in self.table_names]

    def run(self):
        print("Starting ExtractFromDB task...")
        # Create a SQLAlchemy engine
        engine = postgres_engine()

        # Iterate over the table names
        for table_name, output_target in zip(self.table_names, self.output()):
            print(f"Processing table: {table_name}")
            # Read data from the database
            df = read_sql(table_name)

            # Save DataFrame to CSV
            df.to_csv(output_target.path, index=False)
            print(f"Data from table '{table_name}' saved to {output_target.path}")



# FOR DEBUG
# if __name__ == '__main__':
#     print("Starting Luigi pipeline...")
#     luigi.build([ExtractFromJson(), ExtractFromDB()], local_scheduler=True)