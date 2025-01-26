import pandas as pd
import luigi
import luigi.format  # Add this import
import matplotlib.pyplot as plt
from module.Extract import *
import os
import tempfile

def inner_join(df1, df2, key):
    merged_df = pd.merge(df1, df2, on=key, how='inner')
    return merged_df

def handling_col(df):
    if 'first_name' in df.columns and 'last_name' in df.columns:
        df['full_name'] = df['first_name'] + ' ' + df['last_name']
    
    if 'total_price' in df.columns:
        df['currency'] = 'IDR'
    
    if 'email' in df.columns:
        df['email_domain'] = df['email'].str.split('@').str[1]
    
    return df

def select_col(df):
    selected_columns = [
        'reservation_id', 'full_name', 'email', 'email_domain', 'reservation_date',
        'payment_date', 'start_date', 'end_date', 'total_price', 'currency',
        'provider', 'payment_status'
    ]
    existing_columns = [col for col in selected_columns if col in df.columns]
    return df[existing_columns]

def check_missing_value(df):
    missing_values = df.isnull().sum()
    missing_percentage = (missing_values / len(df)) * 100
    missing_info = pd.DataFrame({
        'Missing Values': missing_values,
        'Missing Percentage': missing_percentage
    })
    return missing_info

def visualize_missing_values(df):
    missing_info = check_missing_value(df)
    missing_info['Missing Percentage'].plot(kind='bar', title='Percentage of Missing Values by Column')
    plt.xlabel('Columns')
    plt.ylabel('Missing Percentage')
    plt.show()

def fill_missing_values(df):
    if 'payment_date' in df.columns:
        df['payment_date'] = df['payment_date'].fillna('Missing Data')
    return df

class TransformTask(luigi.Task):
    output_path = luigi.Parameter(default="transformed_data.csv")

    def requires(self):
        return {
            'db_data': ExtractFromDB(),
            'json_data': ExtractFromJson()
        }

    def output(self):
        # Specify UTF8 format to open the file in text mode
        return luigi.LocalTarget(self.output_path, format=luigi.format.UTF8)

    def run(self):
        # Load data from the outputs of the required tasks
        try:
            with self.input()['db_data'][0].open() as reservation_file, \
                self.input()['db_data'][1].open() as customer_file:
                data_reservation = pd.read_csv(reservation_file)
                data_customer = pd.read_csv(customer_file)

            with self.input()['json_data'].open() as json_file:
                data_json = pd.read_csv(json_file)
        except FileNotFoundError as e:
            raise Exception(f"Input file not found: {e}")

        # Perform transformations
        df_pre = inner_join(data_customer, data_reservation, 'customer_id')
        data = inner_join(df_pre, data_json, 'reservation_id')
        data = handling_col(data)
        data = select_col(data)

        # Check missing values before filling
        print("Missing values before filling:")
        missing_before = check_missing_value(data)  # Store the result
        print(missing_before)  # Print the result once

        # Visualize missing values
        visualize_missing_values(data)

        # Fill missing values
        data = fill_missing_values(data)

        # Check missing values after filling
        print("Missing values after filling:")
        missing_after = check_missing_value(data)  # Store the result
        print(missing_after)  # Print the result once

        # Save the transformed data to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp_file:
            data.to_csv(tmp_file, index=False)
            tmp_file_path = tmp_file.name

        # Move the temporary file to the final destination
        with self.output().open('w') as output_file:
            with open(tmp_file_path, 'r') as tmp_file:
                output_file.write(tmp_file.read())

        # Clean up the temporary file
        os.remove(tmp_file_path)

        print(f"Transformed data saved to {self.output_path}")

# FOR DEBUG
# if __name__ == '__main__':
#     print("Starting Luigi pipeline...")
#     luigi.build([TransformTask()], local_scheduler=True)