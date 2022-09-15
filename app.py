""" flask app that shows plotly graphs created from models"""
import re
from flask import Flask, render_template, request
from map_view import run as run_view,get_title,plot_bars
from model import run_last_month as run_model, run_months, run_multi as run_multi_model,get_province_names, get_last_month, get_available_months,save_predictions

""" flask app"""

app = Flask(__name__)


@app.route('/')
def index():
    provinces = get_province_names()
    args = dict(request.args)
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

@app.route('/months')
def index2():
    provinces = get_province_names()
    args = dict(request.args)
    months = get_available_months(True,False)
    """ sort months by year and month """
    months = sorted(months,key=lambda x: (x[1],x[0]))
    if (len(args) == 0):
        return render_template('index.html',provinces = provinces,months = months)
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
    sale = 1 if request.args.get('sale')=='1' else 0
    provinces_list = request.args.get('provinces') if request.args.get('provinces') else 'all'
    months_list = request.args.get('months') if request.args.get('months') else 'all'
    if months_list == 'all':
        months_list = months
    else:
        months_list = months_list.split(',')
        months_list = [(int(x.split('-')[0]),int(x.split('-')[1])) for x in months_list]
    prices = run_months(house_properties,province,1 - sale,months_list)
    
    month, year = get_last_month(province,1 - sale)
    
    if provinces_list != 'all':
        provinces_list = provinces_list.split(',')
        prices = prices[prices["location_name"].isin(provinces_list)]
    title = get_title(house_properties)
    result = run_view(prices,title,as_json=True,slider_col="date")
    rentorsale = "alquiler" if  sale == 0 else "venta"
    bars = plot_bars(prices,as_json=True)
    prices["mínimo"] = prices["min"]
    prices["máximo"] = prices["max"]
    prices["medio"] = prices["middle"]
    prices = prices[["mínimo","máximo","medio","provincia"]]
    prices_html = prices.to_html(classes="table table-striped table-bordered table-hover",index=False)
    return render_template('index.html',graphJSON=result,bars = bars,rentorsale = rentorsale,prices_html = prices_html,provinces = provinces,month = month,year = year,months = months,months_list = months_list)

@app.route('/graph')
def graph():
    args = dict(request.args)
    if (len(args) == 0):
        return render_template('index.html')
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
    sale = 1 if request.args.get('sale')=='1' else 0
    prices = run_multi_model(house_properties,province,1 - sale,"type",["piso","casa","apartamento","ático","dúplex","estudio","loft","finca"])
    title = get_title(house_properties)
    result = run_view(prices,title,as_json=True,slider_col="type")
    rentorsale = "alquiler" if  sale == 0 else "venta"
    bars = plot_bars(prices,as_json=True)
    prices["mínimo"] = prices["min"]
    prices["máximo"] = prices["max"]
    prices["medio"] = prices["middle"]
    prices = prices[["mínimo","máximo","medio","provincia","type"]]
    prices_html = prices.to_html(classes="table table-striped table-bordered table-hover",index=False)
    return render_template('index.html',graphJSON=result,bars = bars,rentorsale = rentorsale,prices_html = prices_html)

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port="9000")
    # app.run(host='