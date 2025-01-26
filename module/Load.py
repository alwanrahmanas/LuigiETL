import luigi
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from module.Transform import TransformTask  # Ensure TransformTask is imported

# Load environment variables from .env file
load_dotenv("Week 8/.env")

def create_db_engine():
    """
    Create and return a SQLAlchemy engine for a Neon PostgreSQL database.

    Returns:
        sqlalchemy.engine.Engine: A SQLAlchemy engine object.
    """
    # Fetch environment variables
    db_user = os.getenv('DB_USER_Neon')
    db_password = os.getenv('DB_PASSWORD_Neon')
    db_host = os.getenv('DB_HOST_Neon')
    db_name = os.getenv('DB_NAME_Neon')
    db_sslmode = os.getenv('DB_SSLMODE_Neon', 'require')  # Default SSL mode

    # Create the database URL (no port needed for Neon)
    database_url = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}?sslmode={db_sslmode}'

    # Create and return the engine
    engine = create_engine(database_url)
    return engine

class LoadData(luigi.Task):
    """
    Luigi task to load transformed data into a Neon PostgreSQL database.
    """
    table_name = luigi.Parameter(default="transformed_data")  # Name of the table in Neon

    def requires(self):
        # Define dependencies
        return TransformTask()  # TransformTask generates the transformed data

    def output(self):
        # Define a dummy output to mark task completion
        return luigi.LocalTarget("load_data_complete.txt")

    def run(self):
        # Load the transformed data from the output of TransformTask
        with self.input().open() as input_file:
            df = pd.read_csv(input_file)

        # Create a SQLAlchemy engine
        engine = create_db_engine()

        try:
            # Load the DataFrame into the Neon PostgreSQL database
            df.to_sql(self.table_name, engine, if_exists='replace', index=False)
            print(f"Data loaded into table '{self.table_name}' successfully.")

            # Mark task completion by creating a dummy output file
            with self.output().open('w') as f:
                f.write("LoadData task completed successfully.")
        except Exception as e:
            print(f"Error loading data into Neon: {e}")
            raise  # Re-raise the exception to mark the task as failed

# FOR DEBUG
# if __name__ == '__main__':
#     print("Starting Luigi pipeline...")
#     luigi.build([LoadData()], local_scheduler=True)