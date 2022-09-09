import unittest
from prediction_repository import PredictionRepository
import datetime
import pandas as pd

class TestPredictionRepository(unittest.TestCase):

    def setUp(self):
        self.repo = PredictionRepository()

    def test_get_location_id(self):
        location_id = self.repo.get_location_id("Madrid", province=False)
        self.assertEqual(location_id, 78)

        location_id = self.repo.get_location_id("Madrid", province=True)
        self.assertEqual(location_id, 29)

    def test_format_where(self):
        names = ["name", "province"]
        values = ["Madrid", "False"]
        where = self.repo.format_where(names, values)
        self.assertEqual(where, "name = 'Madrid' AND province = 'False'")

    def test_get_prediction_parameters_id(self):
        parameters = {"surface":120,"bedrooms":2,"restrooms":2,"elevator":1,"terrace":1,"floor":2,"type":"piso","rent":1}
        prediction_parameters_id = self.repo.get_prediction_parameters_id(parameters)
        self.assertEqual(prediction_parameters_id, 1)
        parameters = {"surface":1000,"bedrooms":2,"restrooms":2,"elevator":1,"terrace":1,"floor":2,"type":"piso","rent":1}
        prediction_parameters_id = self.repo.get_prediction_parameters_id(parameters)
        self.assertIsNone(prediction_parameters_id, 1)
        

    def test_insert_prediction_parameters(self):
        parameters = {"surface":120,"bedrooms":2,"restrooms":2,"elevator":1,"terrace":1,"floor":2,"type":"piso","rent":1}
        self.repo.insert_prediction_parameters(parameters)
        self.assertEqual(self.repo.get_prediction_parameters_id(parameters), 2)

    def test_get_prediction_price(self):
        parameters = {"surface":100,"bedrooms":2,"restrooms":2,"elevator":1,"terrace":1,"floor":2,"type":"piso","rent":1}
        prediction_price = self.repo.get_prediction_price("Madrid", True, parameters)
        self.assertEqual(prediction_price, (-1, 40000, -1, datetime.date(2022, 7, 2)))
        parameters = {"surface":1000,"bedrooms":2,"restrooms":2,"elevator":1,"terrace":1,"floor":2,"type":"piso","rent":1}
        prediction_price = self.repo.get_prediction_price("Madrid", False, parameters)
        self.assertIsNone(prediction_price)

    def test_insert_prediction_price(self):
        parameters = {"surface":100,"bedrooms":2,"restrooms":2,"elevator":1,"terrace":1,"floor":2,"type":"piso","rent":1}
        prices = {"lower":40000,"middle":50000,"upper":60000}
        self.repo.insert_prediction_price("Barcelona", True, parameters, prices)
        prediction_price = self.repo.get_prediction_price("Barcelona", True, parameters)
        self.assertEqual(prediction_price, (40000, 50000, 60000, datetime.date(2022, 7, 2)))
        prices = {"lower":600000,"middle":800000,"upper":900000}
        self.repo.insert_prediction_price("Madrid", False, parameters, prices)
        prediction_price = self.repo.get_prediction_price("Madrid", False, parameters)
        self.assertEqual(prediction_price, (600000, 800000, 900000, datetime.date(2022, 7, 2)))

    def test_insert_prediction_prices(self):
        predictions = pd.read_csv("data/predictions_provincias_alquiler.csv")
        parameters = {"surface":100,"bedrooms":2,"restrooms":2,"elevator":1,"terrace":1,"floor":2,"type":"piso","rent":1}
        self.repo.insert_prediction_prices(predictions,parameters,True)
        prediction_price = self.repo.get_prediction_price("Zaragoza", True, parameters)
        self.assertEqual(prediction_price, (617,776,930, datetime.date.today()))
    
    def test_get_house_with_price_location_as_df_month(self):
        df = self.repo.get_house_with_price_location_as_df_month(1, True, 2022, 7)
        self.assertEqual(df.shape, (24834, 13))
        df = self.repo.get_house_with_price_location_as_df_month(1, False, 2022, 8)
        self.assertEqual(df.shape, (95494, 13))
        
if __name__ == "__main__":
    unittest.main()