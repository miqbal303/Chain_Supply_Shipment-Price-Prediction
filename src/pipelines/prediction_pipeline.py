import sys
import os
import pandas as pd
from src.exception import CustomException
from src.utils import load_object


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path = os.path.join("artifacts", "model.pkl")
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
            print("Before Loading")
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("After Loading")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds

        except Exception as e:
            raise CustomException(e, sys)


class CustomData:
    def __init__(self,
                 Line_Item_Quantity: float,
                 Pack_Price: float,
                 Weight_Kilograms: float,
                 Unit_Price: float,
                 Brand: str,
                 Dosage_Form: str,
                 Country: str,
                 Dosage: str,
                 Item_Description: str,
                 PO_SO: str
                 ):
        self.Line_Item_Quantity = Line_Item_Quantity
        self.Pack_Price = Pack_Price
        self.Weight_Kilograms = Weight_Kilograms
        self.Unit_Price = Unit_Price
        self.Brand = Brand
        self.Dosage_Form = Dosage_Form
        self.Country = Country
        self.Dosage = Dosage
        self.Item_Description = Item_Description
        self.PO_SO = PO_SO

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "Line_Item_Quantity": [self.Line_Item_Quantity],
                "Pack_Price": [self.Pack_Price],
                "Weight_Kilograms": [self.Weight_Kilograms],
                "Unit_Price": [self.Unit_Price],
                "Dosage_Form": [self.Dosage_Form],
                "Brand": [self.Brand],
                "Country": [self.Country],
                "Dosage": [self.Dosage],
                "Item_Description": [self.Item_Description],
                "PO_SO": [self.PO_SO],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
