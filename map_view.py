import numpy as np
from shapely.affinity import translate
import plotly.express as px
import plotly
import json
import geopandas as gpd
import pandas as pd
from model import load_df_from_db

def get_geodf():
    url = url = 'data/provincias-espanolas.geojson'
    df = gpd.read_file(url)
    return df

def get_prices(filename):
    df = pd.read_csv(filename)
    return df
def format_thousands(df,column):
    df[column+"_str"] = df[column].astype('str').str.replace(r'([0-9]+)([0-9]{6})$',r'\1.\2M',regex=True)
    df[column+"_str"] = df[column+"_str"].str.replace(r'([0-9]{2,})([0-9]{3})$',r'\1.\2k',regex=True)
def prepare_prices(prices):
    prices["lower"]= prices["lower"].astype('float')
    prices["middle"]= prices["middle"].astype('float')
    prices["upper"]= prices["upper"].astype('float')

    prices["lower"]= prices["lower"].astype('int')
    prices["middle"]= prices["middle"].astype('int')
    prices["upper"]= prices["upper"].astype('int')
    prices["max"] =  prices.apply(lambda x: max(x['lower'], x['upper'] , x['middle']), axis=1)
    prices["min"] =  prices.apply(lambda x: min(x['lower'], x['upper'] , x['middle']), axis=1)
    prices["provincia"] = prices["location_name"]
    
def plot_bars(prices,as_json=False,slider_col=None):
    prepare_prices(prices)
    #replace2(prices)
    if slider_col is not None:
        fig = px.bar(prices, x="provincia", y=["min","middle","max"], barmode='group', animation_frame=slider_col,labels={'min':'mínimo','middle':'media','max':'máximo','value':'precio estimado'},title="precios por provincia")
    else:
        fig = px.bar(prices, x="provincia", y=["min","middle","max"], barmode='group', labels={'min':'mínimo','middle':'media','max':'máximo','value':'precio estimado'},title="precios por provincia")
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    newnames = {"min":"Precio mínimo","middle":"Precio medio","max":"Precio máximo"}    
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))
    if as_json:
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig.show()
def replace_province_names(prices):
    to_replace = {
        'Alicante': 'Alacant',
        'Baleares':'Illes Balears',
        'Castellón':'Castelló',
        'Gerona': 'Girona',
        'Guipúzcoa' :'Gipuzcoa',
        'La Coruña': 'A Coruña',
        'Lérida' : 'Lleida',
        'Orense' : 'Ourense',
        'Valencia' : 'València',
        'Vizcaya' : 'Bizkaia',
        'Álava' : 'Araba'
    }
    prices["provincia"] = prices["provincia"].replace(to_replace)

def replace2(provinces):
    to_replace = {
        
        'Gipuzcoa' :'Gipuzkoa',
    }
    provinces["provincia"] = provinces["provincia"].replace(to_replace)

def merge_df_prices(df, prices, extra_column=None):
    df = df[df["provincia"]!= "Ceuta"]
    df = df[df["provincia"]!= "Melilla"]
    replace_province_names(prices)
    if extra_column is not None:
        df = df.merge(prices[['middle','max','min','provincia',extra_column]] , on='provincia')
    else:
        df = df.merge(prices[['middle','max','min','provincia']] , on='provincia')
    replace2(df)

    return df

def move_canarias(df,xoff=3,yoff=6):
    las_palmas = df[df["provincia"]=="Las Palmas"]
    tenerife = df[df["provincia"]=="Santa Cruz de Tenerife"]
    las_palmas_shift = las_palmas.geometry.apply(lambda x: translate(x, xoff=xoff, yoff=yoff))
    tenerife_shift = tenerife.geometry.apply(lambda x: translate(x, xoff=xoff, yoff=yoff))
    df.loc[df["provincia"]=="Las Palmas","geometry"] =las_palmas_shift.geometry
    df.loc[df["provincia"]=="Santa Cruz de Tenerife","geometry"] =tenerife_shift.geometry

def plot(df,title="",as_json=False,slider_col=None):
    if slider_col is not None:
        fig  = px.choropleth(df,locations=df.index,geojson=df.geometry,title=title,color="middle",animation_frame=slider_col,hover_name="provincia",hover_data={"min_str":True,'max_str':True,"middle":True},labels={"middle": "Precio medio","min_str":"Precio mínimo","max_str":"Precio máximo"},width=1000,height=1000,basemap_visible=False)
    else:
        fig  = px.choropleth(df,locations=df.index,geojson=df.geometry,title=title,color="middle",hover_name="provincia",hover_data={"min_str":True,'max_str':True,"middle":True},labels={"middle": "Precio medio","min_str":"Precio mínimo","max_str":"Precio máximo"},width=1000,height=1000,basemap_visible=False)
    fig.update_geos(fitbounds="locations")
    fig.update_layout(modebar_remove=['zoom', 'pan'])
    fig.update_layout(dragmode=False)
    
    fig.update_xaxes(fixedrange=True)
    if as_json:
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
    fig.show()

def siono(x):
    if x:
        return "Sí"
    else:
        return "No"
def get_title(parameters):
    title = "superficie = "+str(parameters['surface'])+" m2, dormitorios = "+str(parameters['bedrooms'])+", baños = "+str(parameters['restrooms'])+", ascensor = "+siono(parameters['elevator'])+", terraza = "+siono(parameters['terrace'])+", planta = "+str(parameters['floor'])+", tipo = "+str(parameters['type'])
    return title
def return_plot_as_json(fig):
    return fig.to_json()


def run(prices = None,title="",as_json=False,slider_col=None):
    df = get_geodf()
    if prices is None:
        prices = get_prices("data/predictions_provincias_alquiler.csv")
    prepare_prices(prices)
    df = merge_df_prices(df, prices,slider_col)
    format_thousands(df,"min")
    format_thousands(df,"max")
    move_canarias(df)
    result = plot(df,title,as_json,slider_col=slider_col)
    return result

if __name__ == "__main__":
    #run()
    provincias = get_geodf()
    #print(provincias.provincia)
    df = load_df_from_db(province=True,rent=True)
    #print(df.location_name.unique())
    for location in df.location_name.unique():
        if location not in provincias.provincia.unique():
            print(location)