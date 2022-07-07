from dbmanager import DBManager
import pandas as pd


class PredictionRepository:
    def __init__(self):
        self.dbmanager = DBManager()
    
    def get_location_id(self, location_name,province):
        province = 1 if province else 0
        location = self.dbmanager.select_data("location", "id", "name = '{}' AND province = {}".format(location_name, province))
        if len(location) == 0:
            return None
        location_id = location[0][0]
        return location_id

    def insert_prediction_parameters(self,parameters):
        names =[]
        values = []
        for key, value in parameters.items():
            names.append(key)
            if type(value) == bool:
                value = 1 if value else 0
            values.append(str(value))
        print("inserting data")    
        self.dbmanager.insert_data("prediction_parameters", ','.join(names),','.join(self.format_values(values)))


    def format_where(self,names,values):
        where = []
        for i in range(len(names)):
            where.append(names[i] + " = '" + str(values[i]) + "'")
        where = ' AND '.join(where)    
        return where

    def format_values(self,parameters):
        values = []
        for value in parameters:
            values.append("'"+str(value)+"'")
        return values

    def get_prediction_price(self,location_name, province, parameters):
        location_id = self.get_location_id(location_name, province)
        prediction_parameters_id = self.get_prediction_parameters_id(parameters)
        if prediction_parameters_id is None:
            return None
        data = self.dbmanager.select_data("prediction_result", "lower_price,middle_price,upper_price, date", "location_id = {} AND prediction_parameters_id = {}".format(location_id, prediction_parameters_id))
        if not data or len(data) == 0:
            return None
        return data[0]

    def insert_prediction_price(self,location_name, province, parameters, prices):
        location_id = self.get_location_id(location_name, province)
        prediction_parameters_id = self.get_prediction_parameters_id(parameters)
        if prediction_parameters_id is None:
            return None
        self.dbmanager.insert_data("prediction_result", "location_id, prediction_parameters_id, lower_price, middle_price, upper_price", "{}, {}, {}, {}, {}".format(location_id, prediction_parameters_id, prices["lower"], prices["middle"], prices["upper"]))
        return True

    def prepare_prices_for_insert(self,df,province,parameters_id):
        
        result = []
        for index, row in df.iterrows():
            location_id = self.get_location_id(row["location_name"], province)
            prices = [str(location_id),str(parameters_id),str(round(row["lower"])),str(round(row["middle"])),str(round(row["upper"]))]
            prices = "({})".format(",".join(self.format_values(prices)))
            result.append(prices)
        result = ",".join(result)
        return result

    def insert_prediction_prices(self,prices_data,parameters,province):
        self.insert_prediction_parameters(parameters)
        parameters_id = self.get_prediction_parameters_id(parameters)
        data = self.prepare_prices_for_insert(prices_data,province,parameters_id)
        self.dbmanager.insert_data("prediction_result", "location_id, prediction_parameters_id, lower_price, middle_price, upper_price", data,multiple=True)

    def get_prediction_parameters_id(self,parameters):
        names =[]
        values = []
        for key, value in parameters.items():
            names.append(key)
            if type(value) == bool:
                value = 1 if value else 0
            values.append(value)
        where = self.format_where(names, values)
        data = self.dbmanager.select_data("prediction_parameters", "id", where)
        if len(data) == 0:
            return None
        return data[0][0]
    
    def get_prediction_prices_as_df(self, province, parameters):
        prediction_parameters_id = self.get_prediction_parameters_id(parameters)
        data = self.dbmanager.select_data("predicted_prices", "lower,middle,upper, name,rent,province, date", "parameters_id = {} AND province={} AND date > DATE_SUB(NOW(), INTERVAL 1 MONTH)".format(prediction_parameters_id,province))
        if not data or len(data) == 0:
            return None
        df = pd.DataFrame(data, columns=["lower", "middle", "upper","name","rent","province", "date"])
        return df

    def get_house_with_price_location_as_df(self,province,rent):
        province = 1 if province else 0
        rent = 1 if rent else 0
        data = self.dbmanager.select_data("house_with_price_location", "id,title,price,surface,bedrooms,restrooms,features,description,url,rent,date,location_name,is_province", "is_province={} AND rent={} AND date > DATE_SUB(NOW(), INTERVAL 1 MONTH)".format(province,rent))
        if not data or len(data) == 0:
            return None
        df = pd.DataFrame(data, columns=["id","title","price","surface","bedrooms","restrooms","features","description","url","rent","date","location_name","is_province"])
        return df

if __name__ == "__main__":
    parameters ={
        'surface' : 80,
        'bedrooms' : 2,
        'restrooms' : 2,
        'elevator' : 1,
        'terrace' : 0,
        'floor' : 4,
        'type' : "apartamento",
        'rent' : 1

    }
    prediction_repository = PredictionRepository()
    prices = prediction_repository.get_prediction_prices_as_df(province = 0, parameters = parameters)
    print(prices.head())
    houses = prediction_repository.get_house_with_price_location_as_df(province = 0, rent = 1)
    print(houses.shape)
    print(houses.head())
