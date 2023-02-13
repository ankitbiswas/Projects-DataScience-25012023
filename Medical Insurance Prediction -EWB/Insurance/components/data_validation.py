# Data type
# Unwanted data finding
# data cleaning
from Insurance.entity import artifact_entity
from Insurance.entity import config_entity
from Insurance.exception import InsuranceException
from Insurance.logger import logging
import pandas as pd
import os,sys
from typing import Optional
from scipy.stats import ks_2samp
import numpy as np
from Insurance.config import TARGET_COLUMN
from Insurance.utils import convert_columns_float
from Insurance.utils import write_yaml_file

class DataValidation:
    def __init__(self,data_validation_config:config_entity.DataValidationConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            #logging(f'****************Data Validation*************')
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()
        except Exception as e:
            raise InsuranceException(e,sys)
    
    def drop_missing_values_column(self,df:pd.DataFrame,report_key_name: str)->Optional[pd.DataFrame]:
        try:
            threshold = self.data_validation_config.missing_threshold
            null_report = df.isna().sum()/df.shape[0]
            drop_columns_names = null_report[null_report>threshold].index

            self.validation_error[report_key_name] = list(drop_columns_names)  

            df.drop(list(drop_columns_names),axis=1,inplace=True)

            if len(df.columns) == 0:
                return None
            return df

        except Exception as e:
            raise InsuranceException(e,sys)



    def is_required_columns_exist(self, base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
            base_columns = base_df
            current_columns = current_df

            missing_columns = []

            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f"Column: [{base_column} is not available]")
                    missing_columns.append(base_column)

            if(len(missing_columns)>0):
                self.validation_error[report_key_name] = missing_columns
                return False
            else:
                return True 


        except Exception as e:
            raise InsuranceException(e,sys)

    #
    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report = dict()
            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data,current_data = base_df[base_column],current_df[base_column]

                same_distribution = ks_2samp(base_data,current_data)

                if(same_distribution.pvalue > 0.05):
                    # Null hypothesis accept 
                    drift_report[base_column] = {
                        "pvalues": float(same_distribution.pvalue),
                        "same_distribution":True
                    }
                else:
                    drift_report[base_column] = {
                        "pvalues": float(same_distribution.pvalue),
                        "same_distribution":True
                    }
            
            self.validation_error[report_key_name] = drift_report


        except Exception as e:
            raise InsuranceException(e,sys)
        

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na":np.NAN},inplace=True)
            base_df = self.drop_missing_values_column(df=base_df,report_key_name="Missing Values within Base dataset")

            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            train_df = self.drop_missing_values_column(df=train_df,report_key_name="Missing Values within Train dataset")
            test_df = self.drop_missing_values_column(df=test_df,report_key_name="Missing Values within Test dataset")

            exclude_columns = [TARGET_COLUMN]

            base_df = convert_columns_float(df=base_df,exclude_columns=exclude_columns)
            train_df = convert_columns_float(df=train_df,exclude_columns=exclude_columns)
            test_df = convert_columns_float(df=test_df,exclude_columns=exclude_columns)

            train_df_columns_status = self.is_required_columns_exist(base_df=base_df,current_df=train_df,report_key_name="Missing Columns within Train dataset")
            test_df_columns_status = self.is_required_columns_exist(base_df=base_df,current_df=test_df,report_key_name="Missing Columns within Test dataset")
            
            if train_df_columns_status:
                self.data_drift(base_df=base_df,current_df=train_df,report_key_name="Data_Drift_Within_Train_Dataset")

            if test_df_columns_status:
                self.data_drift(base_df=base_df,current_df=test_df,report_key_name="Data_Drift_Within_Test_Dataset")

            #write your report
            write_yaml_file(file_path=self.data_validation_config.report_file_path,data=self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path = self.data_validation_config.report_file_path)
            print(data_validation_artifact)
            return data_validation_artifact


        except Exception as e:
            raise InsuranceException(e,sys)
