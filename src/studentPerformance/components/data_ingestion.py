
import os
import urllib.request as request
import zipfile
from studentPerformance.logger import logging
from studentPerformance.utils.common import get_size
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from studentPerformance.logger import logging
from sklearn.model_selection import train_test_split
import pandas as pd
# import requests
import urllib
import sys



class DataIngestion:
    def __init__(self, data_ingestion_config):
        self.config = data_ingestion_config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = urllib.request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            print(f"{filename} downloaded with the following info:\n{headers}")
        else:
            print(f"File already exists of size: {os.path.getsize(self.config.local_data_file)}")

    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)

    def ingest_data(self):
        logging.info("Ingestion of the data is initiated")

        raw_data_path = os.path.join(self.config.unzip_dir, "raw_data.csv")
        train_data_path = os.path.join(self.config.unzip_dir, "train_data.csv")
        test_data_path = os.path.join(self.config.unzip_dir, "test_data.csv")

        data_files = os.listdir(self.config.unzip_dir)
        csv_files = [file_name for file_name in data_files if file_name.endswith(".csv")]

        if len(csv_files) == 0:
            raise ValueError("No CSV files found in the unzip directory.")

        df = None
        for file_name in csv_files:
            file_path = os.path.join(self.config.unzip_dir, file_name)
            if df is None:
                df = pd.read_csv(file_path)
            else:
                df = pd.concat([df, pd.read_csv(file_path)], ignore_index=True)

        # Save the raw data
        df.to_csv(raw_data_path, index=False, header=True)

        # Train test split
        train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

        # Save the train and test data
        train_set.to_csv(train_data_path, index=False, header=True)
        test_set.to_csv(test_data_path, index=False, header=True)

        logging.info("Ingestion of the data is completed")

        return train_data_path, test_data_path

