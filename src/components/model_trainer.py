import os
import sys
from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object, evaluate_models

from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()


    def initiate_model_training(self,train_array,test_array):
        try:
            logging.info("Splitting training and test data inputs")
            X_train, y_train, X_test, y_test = (
                train_array.iloc[:, :-1].values,
                train_array.iloc[:, -1].values,
                test_array.iloc[:, :-1].values,
                test_array.iloc[:, -1].values
            )


            models = {
                "Random Forest": RandomForestRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
            params = {
                    'Random Forest': {
                        'n_estimators': [50, 100, 200],
                        'max_depth': [3, 5, 7],
                        'min_samples_split': [2, 5, 10],
                        'min_samples_leaf': [1, 2, 4]
                    },
                    'Gradient Boosting': {
                        'n_estimators': [50, 100, 200],
                        'learning_rate': [0.1, 0.05, 0.01],
                        'max_depth': [3, 5, 7],
                        'min_samples_split': [2, 5, 10],
                        'min_samples_leaf': [1, 2, 4]
                    },
                    'AdaBoost Regressor': {
                        'n_estimators': [50, 100, 200],
                        'learning_rate': [0.1, 0.05, 0.01]
                    },
                    "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                    },
                    'XGBRegressor': {
                        'n_estimators': [50, 100, 200],
                        'learning_rate': [0.1, 0.05, 0.01],
                        'max_depth': [3, 5, 7],
                        'min_child_weight': [1, 3, 5]
                    }
                }
                

            model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,
                                             models=models,param=params)
            
            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]
            

            

            if best_model_score<0.6:
                raise CustomException("No best model found")
            

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)
            logging.info(f"Best found model is {best_model}, R2 Score : {r2_square}")
            print(f'Best Model Found , Model Name : {best_model} , R2 Score : {r2_square}')
            return r2_square
            



            
        except Exception as e:
            raise CustomException(e,sys)