
from map_view import run as run_view,get_title,plot_bars
import model



def get_province_names():
    provinces = model.get_province_names()
    return provinces


def get_available_dates():
    months = model.get_available_months(True,False)
    months = sorted(months,key=lambda x: (x[1],x[0]),reverse=False)
    return months

def get_house_properties(args):
    house_properties = {
        "surface" : args.get('surface'),
        "bedrooms" : args.get('bedrooms'),
        "restrooms" : args.get('restrooms'),
        "elevator" : args.get('elevator',0),
        "terrace" : args.get('terrace',0),
        "floor" : args.get('floor'),
        "type" : args.get('type')
    }
    return house_properties

def is_province(args):
    province = args.get('province')
    return province
    
def is_rent(args):
    rent = args.get('rent','1')
    rent = 1 if rent == '1' else 0
    return rent

def get_selected_provinces(args):
    selected_provinces = args.get('provinces','all') 
    if selected_provinces != 'all':
        selected_provinces = selected_provinces.split(',')
    return selected_provinces

def get_selected_dates(args):
    selected_dates = args.get('dates','all')
    if selected_dates == 'all':
        selected_dates = get_available_dates()
    else:
        selected_dates = selected_dates.split(',')
        selected_dates = [(int(x.split('/')[0]),int(x.split('/')[-1])) for x in selected_dates]
        selected_dates = sorted(selected_dates,key=lambda x: (x[1],x[0]),reverse=False)
    return selected_dates

def predict(args):
    house_properties = get_house_properties(args)
    province = is_province(args)
    rent = is_rent(args)
    selected_provinces = get_selected_provinces(args)
    selected_dates = get_selected_dates(args)
    prices = model.run_months(house_properties,province,rent,selected_dates)
    if selected_provinces != 'all':
        prices = prices[prices["location_name"].isin(selected_provinces)]
    # prices["mínimo"] = prices["min"]
    # prices["máximo"] = prices["max"]
    # prices["medio"] = prices["middle"]
    # prices["fecha"] = prices["date"]
    # prices = prices[["mínimo","máximo","medio","provincia","fecha"]]
    return prices

def plot_map(house_properties,prices):
    title = get_title(house_properties)
    return run_view(prices,title,as_json=True,slider_col="date")

def plot_bars(prices):
    title = get_title(prices)
    model.plot_bars(prices,title)

"""
def predict(args):
    provinces = get_province_names()
    months = get_available_months(True,False)
    months = sorted(months,key=lambda x: (x[1],x[0]),reverse=False)
    if (len(args) == 0):
        return render_template('index.html',provinces = provinces,dates = months)
    house_properties = {
        "surface" : request.args.get('surface'),
        "bedrooms" : request.args.get('bedrooms'),
        "restrooms" : request.args.get('restrooms'),
        "elevator" : request.args.get('elevator') if request.args.get('elevator') else 0,
        "terrace" : request.args.get('terrace') if request.args.get('terrace') else 0,
        "floor" : request.args.get('floor'),
        "type" : request.args.get('type')
    }
    province = request.args.get('province')  if request.args.get('province') else 0
    rent = 1 if request.args.get('rent')=='1' else 0

    months = get_available_months(province=province,rent = rent)
    months = sorted(months,key=lambda x: (x[1],x[0]),reverse=False)
    provinces_list = request.args.get('provinces') if request.args.get('provinces') else 'all'

    months_list = request.args.get('dates') if request.args.get('dates') else 'all'
    if months_list == 'all':
        months_list = months
    else:
        months_list = months_list.split(',')
        months_list = [(int(x.split('/')[0]),int(x.split('/')[-1])) for x in months_list]
        months_list = sorted(months_list,key=lambda x: (x[1],x[0]),reverse=False)
    prices = run_months(house_properties,province,rent,months_list)
    month, year = get_last_month(province,rent)
    
    if provinces_list != 'all':
        provinces_list = provinces_list.split(',')
        prices = prices[prices["location_name"].isin(provinces_list)]

    
    title = get_title(house_properties)
    #save_predictions(prices,"predictions")
    result = run_view(prices,title,as_json=True,slider_col="date")
    
    rentorsale = "alquiler" if  rent == 1 else "venta"
    bars = plot_bars(prices,as_json=True,slider_col="date")
    prices["mínimo"] = prices["min"]
    prices["máximo"] = prices["max"]
    prices["medio"] = prices["middle"]
    prices["fecha"] = prices["date"]
    prices = prices[["mínimo","máximo","medio","provincia","fecha"]]
    prices = prices.sort_values(by=["provincia","fecha"])
    prices_html = prices.to_html(classes="table table-striped table-bordered table-hover",index=False)
    return render_template('index.html',graphJSON=result,bars = bars,rentorsale = rentorsale,prices_html = prices_html,provinces = provinces,month = month,year = year,dates = months,dates_list = months_list)

"""