from src.studentPerformance.config.configuration import ConfigurationManager
from src.studentPerformance.components.data_ingestion import DataIngestion
from src.studentPerformance.components.data_validation import DataValidation
from src.studentPerformance.logger import logging


class DataValidationTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_all_files_exist()