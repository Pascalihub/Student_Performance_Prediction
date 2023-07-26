from src.studentPerformance.config.configuration import ConfigurationManager
from src.studentPerformance.components.data_ingestion import DataIngestion
from src.studentPerformance.logger import logging


class DataIngestionTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()
        train_data_path, test_data_path = data_ingestion.ingest_data()