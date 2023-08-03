import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # Read the dataset as dataframe
            data_path = 'notebook\dataset\SCMS_Delivery_History_Dataset.csv'
            df = pd.read_csv(data_path)
            logging.info('Read the dataset as dataframe')

            # Data cleaning
            df = df[df['Weight (Kilograms)'] != 'Weight Captured Separately']
            df = df[df['Freight Cost (USD)'] != 'Freight Included in Commodity Cost']
            df = df[df['Freight Cost (USD)'] != 'Invoiced Separately']
            df = df[~df[['Weight (Kilograms)', 'Freight Cost (USD)']].apply(lambda row: row.astype(str).str.contains('See').any(), axis=1)]
            df[['Weight (Kilograms)', 'Freight Cost (USD)']] = df[['Weight (Kilograms)', 'Freight Cost (USD)']].apply(pd.to_numeric)
            df['Dosage'] = df['Dosage'].fillna(df['Dosage'].mode()[0])
            df['Line Item Insurance (USD)'] = df['Line Item Insurance (USD)'].fillna(df['Line Item Insurance (USD)'].median())
            df['Total Cost'] = df['Line Item Value'] + df['Line Item Insurance (USD)'] + df['Freight Cost (USD)']
            df = df[['Line Item Quantity', 'Pack Price', 'Weight (Kilograms)', 'Unit Price', 'Brand', 'Dosage Form', 'Country', 'Dosage', 'Item Description', 'PO / SO #', 'Total Cost']]

            # Renaming columns
            original_columns = ['Line Item Quantity', 'Pack Price', 'Weight (Kilograms)', 'Unit Price', 'Brand', 'Dosage Form', 'Country', 'Dosage', 'Item Description', 'PO / SO #', 'Total Cost']
            new_columns = {col: col.replace(' ', '_') for col in original_columns}
            df.rename(columns=new_columns, inplace=True)
            df['Weight_Kilograms'] = df['Weight_(Kilograms)']
            df['PO_SO'] = df['PO_/_SO_#']
            df.drop(['Weight_(Kilograms)', 'PO_/_SO_#'], axis=1, inplace=True)  # Remove redundant columns
            total_cost = df['Total_Cost']
            df.drop('Total_Cost', axis=1, inplace=True)
            df['Total_Cost'] = total_cost

            # Save the raw data
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Data transformation and cleaning completed. Raw data saved.")

            # Train-test split
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save the train and test datasets
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Train-test split completed. Train and test datasets saved.")

            return self.ingestion_config.train_data_path, self.ingestion_config.test_data_path

        except Exception as e:
            logging.error("Error occurred during ingestion of the data")
            raise CustomException(e, sys)
        