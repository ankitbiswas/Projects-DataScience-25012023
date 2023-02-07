from Insurance.logger import logging
from Insurance.exception import InsuranceException
import os, sys
from Insurance.utils import get_collection_as_dataframe
from data_dump import DATABASE_NAME,COLLECTION_NAME
from Insurance.entity.config_entity import DataIngestionConfig
from Insurance.entity import config_entity
from Insurance.components.data_ingestion import DataIngestion

# def test_logger_and_exception():
    # try:
    #     logging.info("Starting the test_logger_and_exception")
    #     result = 3/0
    #     print(result)
    #     logging.info("Ending the test_logger_and_exception")
    # except Exception as e:
    #     logging.debug(str(e))
    #     raise InsuranceException(e,sys)


if __name__ == "__main__":
    try:
        # get_collection_as_dataframe(database_name=DATABASE_NAME,collection_name=COLLECTION_NAME)
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config)
        print(data_ingestion_config.to_dict())

        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
    except Exception as e:
        print(e)