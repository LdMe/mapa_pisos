import threading
from model import load_csv,clean_df,create_predictors_per_location,save_predictors,load_predictors,get_price_for_houses_multiple_predictors,save_predictions,save_predictions_to_db,load_df_from_db,run_multi,load_df_from_csv
from sys import argv
from map_view import run as run_view
import pandas as pd

def translate_parameters(parameters,args):
    for i in range(len(args)):
        if get_true_param(parameters,'sale',args[i]): continue
        if get_true_param(parameters,'province',args[i]): continue
        if get_true_param(parameters,'build',args[i]): continue
        if get_true_param(parameters,'save',args[i]): continue
        if get_true_param(parameters,'show',args[i]): continue

        if get_param_value(parameters,'surface',args[i],isint=True): continue
        if get_param_value(parameters,'bedrooms',args[i],isint=True): continue
        if get_param_value(parameters,'restrooms',args[i],isint=True): continue
        if get_param_value(parameters,'elevator',args[i],isint=True): continue
        if get_param_value(parameters,'terrace',args[i],isint=True): continue
        if get_param_value(parameters,'floor',args[i],isint=True): continue
        if get_param_value(parameters,'type',args[i]): continue
    return parameters

def get_true_param(parameters,param,arg):
    if arg == param:
        parameters[param] = True
        return True
    return False


def get_param_value(parameters,param,arg,isint=False):
    if param in arg:
        result = arg.split(param+"=")[1]
        if isint:
            result = int(result)
        parameters[param] = result 
        return True
    return False

def get_filename(province,sale,root="data/",extension=""):
    location = "provincias" if province else "capitales"
    sale = "compra" if sale else "alquiler"
    return root+location+"_"+sale+extension

def siono(value):
    return "si" if value else "no"
def get_multiple_prices():
    predictors = load_predictors(get_filename(True,False,"data/predictors_", ".pkl"))
    house_properties = {
        "surface" : 100,
        "bedrooms" : 2,
        "restrooms" : 2,
        "elevator" : 1,
        "terrace" : 1,
        "floor" : 2,
        "type" : 'piso',
        "rent" : 1
    }
    price_df = run_multi(house_properties,True,True,"surface",range(40,210,10))
    
    return price_df
def run(parameters,from_db=True):
    #df = load_csv(get_filename( parameters['province'],parameters['sale']))
    
    if parameters['build']:
        if from_db:
            df = load_df_from_db(province=parameters['province'],rent= not parameters['sale'])
        else:
            df = load_df_from_csv(province=parameters['province'],rent= not parameters['sale'])
        df = clean_df(df)
        predictors = create_predictors_per_location(df)
        save_predictors(predictors,get_filename(parameters['province'],parameters['sale'],"data/predictors_",".pkl"))
    else:
        predictors = load_predictors(get_filename(parameters['province'],parameters['sale'],"data/predictors_", ".pkl"))
    house_properties = {
        "surface" : parameters['surface'],
        "bedrooms" : parameters['bedrooms'],
        "restrooms" : parameters['restrooms'],
        "elevator" : parameters['elevator'],
        "terrace" : parameters['terrace'],
        "floor" : parameters['floor'],
        "type" : parameters['type'],
        "rent" : not parameters['sale']
    }
    price_df = get_price_for_houses_multiple_predictors(predictors,house_properties,parameters["province"])
    print(price_df)
    if parameters["save"]:
        save_predictions(price_df,get_filename(parameters['province'],parameters['sale'],"data/predictions_"))
        save_predictions_to_db(price_df,house_properties,parameters['province'])
    if parameters['show']:
        title = "superficie = "+str(parameters['surface'])+" m2, dormitorios = "+str(parameters['bedrooms'])+", baños = "+str(parameters['restrooms'])+", ascensor = "+siono(parameters['elevator'])+", terraza = "+siono(parameters['terrace'])+", planta = "+str(parameters['floor'])+", tipo = "+str(parameters['type'])
        run_view(price_df,title)
    print("Predictions saved")
    return price_df

""" function to save predictors for a specific month and year"""
def build_and_save_month(province,rent,month,year):
    df = load_df_from_db(province,rent,[month,year])
    df = clean_df(df)
    predictors = create_predictors_per_location(df)
    save_predictors(predictors,get_filename(province,rent,"data/predictors_","_"+str(month)+"-"+str(year)+".pkl"))

""" function to create and save predictions for each month of a time range """
def run_monthly(province,rent,time_range):
    for month, year in time_range:
        """ run build and save month  in separate thread """
        thread = threading.Thread(target=build_and_save_month, args=(province,rent,month,year))
        thread.start()


if __name__ == "__main__":
    
    parameters = {
        'sale' : False,
        'province' : False,
        'surface' : 100,
        'bedrooms' : 2,
        'restrooms' : 2,
        'elevator' : 1,
        'terrace' : 0,
        'floor' : 4,
        'type' : "piso",
        'build' : False,
        'save' : False,
        'show' : False
    }

    if len(argv) > 1:
        parameters = translate_parameters(parameters,argv[1:])

    #prices = run(parameters,from_db=False)

    run_monthly(False,True,[[7,2022],[8,2022],[9,2022]])
    run_monthly(False,False,[[7,2022],[8,2022],[9,2022]])
