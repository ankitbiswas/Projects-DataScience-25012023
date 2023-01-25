import pymongo 
import pandas as pd
import json 
import numpy as np


client = pymongo.MongoClient("mongodb+srv://ankitbiswas008:Feb2019@cluster0.8kx7krt.mongodb.net/?retryWrites=true&w=majority")
db = client.test

DATA_FILE_PATH = (r"C:\DataScience-Learnbay\DataScience-Learnbay\Excel\Projects\Git_25012023\Projects-DataScience-25012023\Medical Insurance Prediction -EWB\insurance.csv")

DATABASE_NAME ="INSURANCE"

COLLECTION_NAME = "INSURANCE_PROJECT"

if __name__ == "__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns: ",df.shape)
    
    df.reset_index(drop=True,inplace=True) #dropping indexes

    #Transpose the data as mongo db takes in key value pair
    json_record = list(json.loads(df.T.to_json()).values())

    print(json_record[0])

    #insert to mongodb

    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
    