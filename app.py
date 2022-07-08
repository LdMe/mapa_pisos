""" flask app that shows plotly graphs created from models"""
import re
from flask import Flask, render_template, request
from map_view import run as run_view,get_title,plot_bars
from model import run as run_model, run_multi as run_multi_model,get_province_names

""" flask app"""

app = Flask(__name__)


@app.route('/')
def index():
    provinces = get_province_names()
    args = dict(request.args)
    if (len(args) == 0):
        return render_template('index.html',provinces = provinces)
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
    
    prices = run_model(house_properties,province,1 - sale)
    if provinces_list != 'all':
        provinces_list = provinces_list.split(',')
        prices = prices[prices["location_name"].isin(provinces_list)]
    title = get_title(house_properties)
    result = run_view(prices,title,as_json=True)
    rentorsale = "alquiler" if  sale == 0 else "venta"
    bars = plot_bars(prices,as_json=True)
    prices["mínimo"] = prices["min"]
    prices["máximo"] = prices["max"]
    prices["medio"] = prices["middle"]
    prices = prices[["mínimo","máximo","medio","provincia"]]
    prices_html = prices.to_html(classes="table table-striped table-bordered table-hover",index=False)
    return render_template('index.html',graphJSON=result,bars = bars,rentorsale = rentorsale,prices_html = prices_html,provinces = provinces)

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