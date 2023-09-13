
import os
from src.studentPerformance.logger import logging
import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler,OrdinalEncoder
import pickle
from src.studentPerformance.entity import DataTransformationConfig




class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def get_data_transformer_obj(self):
        '''
        This function is responsible for data transformation
        '''
        try:
            # Define which columns should be ordinal-encoded and which should be scaled
            numerical_columns=['writing_score','reading_score']
            categorical_columns=[
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]
            
            # Define the custom ranking for each ordinal variable
            gender = ['female', 'male']
            race_ethnicity = ['group B', 'group C', 'group A', 'group D', 'group E']
            parental_level_of_education = ["bachelor's degree", "some college", "master's degree", "associate's degree",
            "high school", "some high school"]
            lunch = ['standard', 'free/reduced']
            test_preparation_course = ['none', 'completed']

            # Numerical Pipeline
            num_pipeline = Pipeline(
                steps = [
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())                
                ]
            )

            # Categorical Pipeline
            cat_pipeline = Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('ordinal_encoder',OrdinalEncoder(categories=[gender,
                race_ethnicity,
                parental_level_of_education,
                lunch,
                test_preparation_course])),
                ('scaler',StandardScaler())
                ]
            )

            logging.info(f'Categorical Columns : {categorical_columns}')
            logging.info(f'Numerical Columns   : {numerical_columns}')

            preprocessor = ColumnTransformer(
                [
                ('num_pipeline',num_pipeline,numerical_columns),
                ('cat_pipeline',cat_pipeline,categorical_columns)
                ]
            )
            
            return preprocessor

        except Exception as e:
            logging.error(f"Error in get_data_transformer_object: {str(e)}")

    def initiate_data_transformation(self):
        try:
            train_data_path = 'artifacts/data_ingestion/unzipped_data/train_data.csv'
            test_data_path = 'artifacts/data_ingestion/unzipped_data/test_data.csv'

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            # Read training and test data
            train_df = pd.read_csv(train_data_path)
            test_df = pd.read_csv(test_data_path)

            logging.info('Read train and test data completed')
            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head  : \n{test_df.head().to_string()}')

            logging.info('Obtaining preprocessing object')

            preprocessing_obj = self.get_data_transformer_obj()

            target_column_name = 'math_score'

            # Separate input features and target features
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            # Apply the preprocessing object on training and test input features
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            # Combine input features and target features
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            # Save preprocessing object
            preprocessing_obj_file = os.path.join("artifacts", 'data_transformation', 'preprocessing_obj.pkl')
            with open(preprocessing_obj_file, 'wb') as file:
                pickle.dump(preprocessing_obj, file)

            logging.info("Saved preprocessing object.")
            logging.info("Transformation of the data is completed")
            
            return (
                train_arr,
                test_arr,
                preprocessing_obj_file
            )
        except Exception as e:
            logging.error(f"Error in initiate_data_transformation: {str(e)}")
        




