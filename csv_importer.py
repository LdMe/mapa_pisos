import pandas as pd

def get_houses():
    """ get houses from db """
    houses = pd.read_csv("data/MYSQL/house.csv")
    return houses

def get_locations():
    """ get locations from db """
    locations = pd.read_csv("data/MYSQL/location.csv")
    return locations

def get_prices():
    """ get prices from db """
    prices = pd.read_csv("data/MYSQL/price.csv")
    return prices

def get_house_locations():
    """ get house locations from db """
    house_locations = pd.read_csv("data/MYSQL/house_location.csv")
    return house_locations

def merge_house_prices():
    """ merge house and price """
    houses = get_houses()
    prices = get_prices()
    house_prices = houses.merge(prices[["price","date","rent","house_id"]], left_on="id",right_on="house_id")
    house_prices = house_prices.drop(["house_id"], axis=1)

    return house_prices

def merge_house_locations():
    """ merge house and location """
    houses = merge_house_prices()
    locations = get_locations()
    house_locations = get_house_locations()
    result = houses.merge(house_locations, left_on="id",right_on="house_id")
    result = result.merge(locations[["id","name","province"]], left_on="location_id",right_on="id")
    result = result.drop(["location_id","id_y","house_id"], axis=1)
    return result


def get_houses_final(province=True, rent=True):
    pisos = merge_house_locations()
    pisos = pisos[pisos["province"] == province]
    pisos = pisos[pisos["rent"] == rent]
    rename_dict = {"id_x":"id","name":"location_name","province":"is_province"
    }
    pisos = pisos.rename(columns=rename_dict)
    return pisos



if __name__ == "__main__":
    pisos_alquiler_provincia = get_houses_final(province=True, rent=1)
    print (pisos_alquiler_provincia.info())
    
