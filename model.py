import os
import threading
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor
from prediction_repository import PredictionRepository
from csv_importer import get_houses_final as load_house_csv
import pickle

def encode_one_hot(df,col,prefix=""):
    y = pd.get_dummies(df[col])
    df_cp = df.copy()
    df_cp = df_cp.join(y,rsuffix=prefix)
    return df_cp


def load_csv(file_path):
    df = pd.read_csv(file_path+'.csv')
    return df
def load_df_from_db(province,rent,date = []):
    repo = PredictionRepository()
    if len(date) !=  2:
        df = repo.get_house_with_price_location_as_df(province,rent)
    else:
        df = repo.get_house_with_price_location_as_df_month(province,rent,date[0],date[1])
    return df
def load_df_from_csv(province=True,rent=True):
    return load_house_csv(province,rent)
def clean_df(df):
    
    df = df[df != -1]
    df = df.dropna()
    df_cp = df.copy()
    df_cp = df_cp.drop(["rent","is_province"],axis=1)
    df_cp["elevator"] = df_cp["features"].str.contains("Ascensor") * 1
    df_cp["elevator"] = df_cp["elevator"].astype(str).astype(float)

    df_cp["terrace"] = df_cp["features"].str.contains("Terraza") * 1
    df_cp["terrace"] = df_cp["terrace"].astype(str).astype(float)

    df_cp["floor"] = df_cp["features"].str.extract(r'([0-9]+.\ Planta)',expand = True)
    df_cp["floor"] = df_cp["floor"].str.extract(r'([0-9])',expand = True)
    df_cp["floor"] = df_cp["floor"].astype(str).astype(float)
    df_cp["type"] = df_cp["title"].str.split(" ").str[0].str.lower()
    df_cp.loc[df_cp["type"] == "planta","floor"] = 0
    df_cp.loc[df_cp["type"] == "planta","type"] = "piso"
    df_cp = df_cp[df_cp["floor"].notnull()].copy()
    df_cp = df_cp[df_cp != -1]
    # A evaluar: borrar pisos sin planta (casi la mitad) o poner media / cero
    
    df_cp = fill_missing_values(df_cp,"floor","type","median")

    df_cp = df_cp.dropna()
    if df["rent"].any() == 1:
        df_cp = df_cp[df_cp["price"]< 4000]
    df_cp = df_cp[df_cp["surface"]< 2000]
    df_cp = df_cp[df_cp["surface"]> 29]
    df_cp = df_cp[df_cp["bedrooms"]< 10]
    df_cp = encode_one_hot(df_cp,"location_name")
    df_cp = encode_one_hot(df_cp,"type")
    df_cp = df_cp.drop(["title","features","description","url","date"],axis=1)
    return df_cp

def split(df):
    X = df.drop(["price"],axis=1)
    y = df["price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    train_set = pd.concat([X_train, y_train], axis=1)
    test_set = pd.concat([X_test, y_test], axis=1)
    return train_set,test_set

def fill_missing_values(df,column_to_fill="floor",reference_column="type",type="mean"):

    if type == "mean":
        mapping_values = df[df[column_to_fill].notnull()].groupby(reference_column).mean()
    elif type == "median":
        mapping_values = df[df[column_to_fill].notnull()].groupby(reference_column).median()
    else:
        print("type not valid")
        return df
    mapping_dict = {}
    for element in mapping_values.index:
        mapping_dict[element] = mapping_values[column_to_fill][element]
    mask = df[column_to_fill].isnull()
    df.loc[mask,column_to_fill] = df.loc[mask,reference_column].map(mapping_dict)
    return df


def get_pipeline(predictor, normalization=True):
    """ pipeline with normalization"""
    if normalization:
        pipe = Pipeline([('scl', StandardScaler()),
                         ('clf', predictor)])
    else:
        pipe = Pipeline([('clf', predictor)])
    return pipe

""" calculate intervals for forest regressor"""
def pred_ints(model, X, percentile=80):
    err_down = []
    err_up = []
    predictions = []
    for pred in model.estimators_:
        predictions.append(pred.predict(X))
    predictions = np.array(predictions).T
    for i in range(len(predictions)):
        err_down.append(np.percentile(predictions[i], (100 - percentile)/2. ))
        err_up.append(np.percentile(predictions[i], 100 - (100 - percentile)/2.))
    

    return err_down, err_up





"""   -------------------------------------------"""

"""  calculate interval for gradientBoostingRegressor"""

def create_predictors_gb(lower_alpha=0.1,upper_alpha=0.9,n_estimators=500):
    predictors = {}
    predictors['lower'] = GradientBoostingRegressor(loss="quantile",alpha=lower_alpha,n_estimators=n_estimators)
    predictors['middle'] = GradientBoostingRegressor(loss="quantile",alpha=0.5 ,n_estimators=n_estimators)
    predictors['upper'] = GradientBoostingRegressor(loss="quantile",alpha=upper_alpha,n_estimators=n_estimators)
    return predictors
def pred_ints_gb(models, X):
    predictions = {}
    for model in models:
        predictions[model] = models[model].predict(X)
    predictions = pd.DataFrame(predictions)
    return predictions
def fit_gb(models,X,y):
    for model in models:
        models[model].fit(X,y)
    return models
def create_predictors_per_location(df):
    predictors = {}
    locations = df["location_name"].unique()
    for location in locations:

        print("creating predictors for "+location)
        
        df_location = df[df["location_name"] == location]
        x_location = df_location.drop(["id","type","location_name","price"],axis=1)
        y_location = df_location["price"]
        train_set, test_set = split(df_location)
        print("fitting predictors...")
        predictor = create_predictors_gb()
        fit_gb(predictor,x_location,y_location)
        print("score: "+str(predictor['middle'].score(x_location,y_location)))
        mean_location_x = pd.DataFrame([get_mean_values(x_location)])
        mean_location_y = pd.DataFrame([get_mean_values(y_location)])
        print("mean price: " +str(mean_location_y))
        prediction = predictor['middle'].predict(mean_location_x)
        print("predicted price: " +str(prediction))
        error = abs( (mean_location_y - prediction)/ mean_location_y) 
        print("error: "+ str(error))
        predictors[location] = predictor
        print("------------------------------")
    return predictors


def save_predictors(predictors,file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(predictors, f)

def load_predictors(file_path):
    with open(file_path, 'rb') as f:
        predictors = pickle.load(f)
    return predictors

def get_mean_values(df):
    return df.mean()
def get_province_names():
    return [
        'A Coruña', 'Araba', 'Albacete', 'Alacant', 'Almería', 'Asturias', 'Ávila',
        'Badajoz', 'Illes Balears', 'Barcelona', 'Bizkaia','Burgos', 'Cáceres', 'Cádiz', 'Cantabria',
        'Castelló', 'Ciudad Real', 'Córdoba', 'Cuenca', 'Gipuzkoa','Girona', 'Granada',
        'Guadalajara',  'Huelva', 'Huesca', 'Jaén', 'La Rioja',
        'Las Palmas', 'León', 'Lleida', 'Lugo', 'Madrid', 'Málaga', 'Murcia', 'Navarra',
        'Ourense', 'Palencia', 'Pontevedra', 'Salamanca', 'Santa Cruz de Tenerife',
        'Segovia', 'Sevilla', 'Soria', 'Tarragona', 'Teruel', 'Toledo', 'València',
        'Valladolid',  'Zamora', 'Zaragoza']
def get_capital_names():
    return [
        'A Coruña', 'Albacete', 'Alicante', 'Almería', 'Ávila', 'Badajoz', 'Barcelona',
        'Bilbao', 'Burgos', 'Cáceres', 'Cádiz', 'Castellón de la Plana', 'Ciudad Real',
        'Córdoba', 'Cuenca', 'Girona', 'Granada', 'Guadalajara', 'Huelva', 'Huesca',
        'Jaén', 'Las Palmas de Gran Canaria', 'León', 'Lleida', 'Logroño', 'Lugo',
        'Madrid', 'Málaga', 'Murcia', 'Ourense', 'Oviedo', 'Palencia',
        'Palma de Mallorca', 'Pamplona', 'Pontevedra', 'Salamanca', 'San Sebastián',
        'Santa Cruz de Tenerife', 'Santander', 'Segovia', 'Sevilla', 'Soria',
        'Tarragona', 'Teruel', 'Toledo', 'Valencia', 'Valladolid', 'Vitoria', 'Zamora',
        'Zaragoza']
def get_unique_values(df,column):
    return df[column].unique()

def get_price_for_houses_multiple_predictors(predictors,house_properties,province=True):
    types = ['piso', 'apartamento', 'ático', 'loft', 'dúplex', 'estudio', 'casa',  'finca']
    locations_province = get_province_names()
    locations_capital = get_capital_names()
    locations = locations_province if province else locations_capital    
    if house_properties["type"] not in types:
        print("type not valid")
        print("valid options: " + str(types))
        return -1
    locations.sort()
    location_dict = {location : 0 for location in locations}
    types.sort()
    type_dict = {t : 0 for t in types}
    predictions = []
    for location in locations:
        df_dict = {
            "surface" : [house_properties["surface"]],
            "bedrooms" : [house_properties["bedrooms"]],
            "restrooms" : [house_properties["restrooms"]],
            "elevator" : [house_properties["elevator"]],
            "terrace" : [house_properties["terrace"]],
            "floor" : [house_properties["floor"]],
        }
        location_dict2 = location_dict.copy()
        location_dict2[location] = 1
        type_dict2 =type_dict.copy()
        type_dict2[house_properties["type"]] = 1
        df1 = df_dict | location_dict2 | type_dict2
        df1 = pd.DataFrame.from_dict(df1)
        prediction = pred_ints_gb(predictors[location],df1)
        #prediction = predictors[location].predict(df1)[0]
        prediction["location_name"] = location
        predictions.append(prediction)
    """ merge array of dataframes"""
    predictions = pd.concat(predictions)
    return predictions
def get_unique(df,col):
    return df[col].unique()
def save_predictions(prices,file_path):
    
    prices.to_csv(file_path+'.csv',index=False)



def save_predictions_to_db(prices,house_properties,province):
    print("saving to db")
    prediction_repository = PredictionRepository()
    prediction_repository.insert_prediction_prices(prices,house_properties,province)

def run(house_properties,province,rent):
    predictors = load_predictors(get_filename(province,rent,"data/predictors_", ".pkl"))
    prices = get_price_for_houses_multiple_predictors(predictors,house_properties,province)
    return prices
def run_month(house_properties,province,rent,month,year):
    predictors = load_predictors(get_filename(province,rent,"data/predictors_", "_"+str(month)+"-"+str(year)+".pkl"))
    prices = get_price_for_houses_multiple_predictors(predictors,house_properties,province)
    prices["date"] = str(month)+"/"+str(year)
    return prices
def get_available_months(province,rent):
    """ get list of filenames inside data/"""
    province = "provincias" if province else "capitales"
    rent = "alquiler" if rent else "compra"
    files = os.listdir("./data/")
    files = [f for f in files if f.startswith("predictors_"+province+"_"+rent)]
    """ get month and year from each filename. Example filename: predictors_provincias_alquiler_9-2022.pkl"""
    months = [[f.split("_")[-1].split("-")[0], f.split("_")[-1].split("-")[-1].split(".")[0]] for f in files]
    """ keep only numeric values"""
    for m in months:
        if not m[0].isnumeric() or not m[1].isnumeric():
            months.remove(m)
    return months
def get_last_month(province,rent):
    months = get_available_months(province,rent)
    months.sort(key=lambda x: (x[1],x[0]))
    return months[-1]
def load_last_predictors(province,rent):
    month, year = get_last_month(province,rent)
    return load_predictors(get_filename(province,rent,"data/predictors_", "_"+str(month)+"-"+str(year)+".pkl"))
def run_last_month(house_properties,province,rent):
    predictors = load_last_predictors(province,rent)
    prices = get_price_for_houses_multiple_predictors(predictors,house_properties,province)
    return prices
def run_multi(house_properties,province,rent,column_name,column_values):
    predictors = load_predictors(get_filename(province,rent,"data/predictors_", ".pkl"))
    house_properties[column_name] = column_values[0]
    prices = get_price_for_houses_multiple_predictors(predictors,house_properties,province)
    prices[column_name] = column_values[0]
    for column_value in column_values[1:]:
        house_properties[column_name] = column_value
        prices1 = get_price_for_houses_multiple_predictors(predictors,house_properties,province)
        prices1[column_name] = column_value
        prices = pd.concat([prices,prices1])
    return prices
def get_filename(province,rent,root="data/",extension=""):
    location = "provincias" if province else "capitales"
    sale = "alquiler" if rent else "compra"
    print("filename")
    print(root+location+"_"+sale+extension)
    return root+location+"_"+sale+extension

def run_month_tread(house_properties,province,rent,month,year,results):
    predictors = load_predictors(get_filename(province,rent,"data/predictors_", "_"+str(month)+"-"+str(year)+".pkl"))
    prices = get_price_for_houses_multiple_predictors(predictors,house_properties,province)
    prices["date"] = str(month)+"/"+str(year)
    results.append(prices)
def run_months(house_properties,province,rent,months):
    months = sorted(months,key=lambda x: (x[1],x[0]),reverse=False)
    prices = []
    prices_threads = []
    """ run each month in a different thread and save results in prices array"""
    for month in months:
        """
        prices1 = run_month(house_properties,province,rent,month[0],month[1])
        prices1["date"] = str(month[0])+"/"+str(month[1])
        prices.append(prices1)
        """
        t = threading.Thread(target=run_month_tread, args=(house_properties,province,rent,month[0],month[1],prices))
        t.start()
        prices_threads.append(t)
    """ wait for all threads to finish"""
    for p in prices_threads:
        p.join()
    """ merge all dataframes"""
    #print(prices)
    prices = [p for p in prices if isinstance(p, pd.DataFrame)]
    prices = pd.concat(prices)
    prices = prices.sort_values(by=["date"])
    return prices
if __name__ == '__main__':
    #df = load_csv("data/provincias_alquiler.csv")
    #df = load_df_from_db(province=False,rent=True)
    #df =clean_df(df)
    #print(df["type"].unique())
    #print(df["location_name"].unique())
    months = get_available_months(province=True,rent=True)

    house_properties = {
        "surface" : 50,
        "bedrooms" : 2,
        "restrooms" : 1,
        "elevator" : 1,
        "terrace" : 1,
        "floor" : 1,
        "type" : "casa",
        "rent" : 1
    }
    #print(run_month(house_properties,province=True,rent=True,month=months[0][0],year=months[0][1]))
    #print(months)
    #print(get_last_month(province=True,rent=True))
    get_available_months(province=True,rent=True)
    print(sorted(months,key=lambda x: (x[1],x[0])))
    print(run_months(house_properties,province=True,rent=True,months=months))
    exit()
    for month in months:
        result = run_month(house_properties,province=True,rent=True,month=month[0],year=month[1])
        print(result[result["location_name"]=="Gipuzkoa"], month)
    last = run_last_month(house_properties,province=True,rent=True)
    print(last[last["location_name"]=="Gipuzkoa"])
    exit()
    df = clean_df(df)
    #print(get_unique(df,"location_name"))
    #print(get_unique(df,"type"))
    
    predictors = create_predictors_per_location(df)
    #save_predictors(predictors,"data/predictors_provincias_alquiler.pkl")
    #predictors = load_predictors("data/predictors_provincias_alquiler.pkl")
    house_properties = {
        "surface" : 50,
        "bedrooms" : 2,
        "restrooms" : 1,
        "elevator" : 1,
        "terrace" : 1,
        "floor" : 1,
        "type" : "casa",
        "rent" : 1
    }
    price_dict = get_price_for_houses_multiple_predictors(predictors,house_properties,province=True)
    print(price_dict)
    #save_predictions(price_dict,"data/predicciones_provincias_alquiler")
    
    save_predictions_to_db(price_dict,house_properties,province=True)
    #print("done")