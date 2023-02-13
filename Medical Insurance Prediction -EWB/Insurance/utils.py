import pandas as pd
import numpy as np
import os
import sys

import yaml
from Insurance.exception import InsuranceException
from Insurance.config import mongo_client   
from Insurance.logger import logging
import stat




def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    try:
        logging.info(f"Reading data from {database_name} and {collection_name}")
        df = pd.DataFrame(mongo_client[database_name][collection_name].find())
        logging.info(f"Find columns:{df.columns}")

        if "_id" in df.columns:
            logging.info(f"Dropping _id column")
            df = df.drop(columns='_id')
        logging.info(f"Rows and Columns in df: {df.shape}")
        return df

    except Exception as e:
        raise InsuranceException(e,sys)


def convert_columns_float(df:pd.DataFrame,exclude_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns:
                if df[column].dtypes !='O':
                    df[column]=df[column].astype('float')
        
        return df

    except Exception as e:
        raise InsuranceException(e,sys)

def write_yaml_file(file_path,data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        # os.makedirs(file_dir,exist_ok=True)
        # os.chmod(file_dir, 0o777)
        # with open(file_dir,'w+') as file_write:
        # yaml.dump(data,file_dir)
    except Exception as e:
        raise InsuranceException(e,sys)
