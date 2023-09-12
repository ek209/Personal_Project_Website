from flask import Blueprint, request, redirect
import sqlite3
import os
import pandas as pd



DB_URL = os.environ.get('RF_DB_URI')

redfin_api_home = Blueprint('redfin_api_home', __name__,
                        template_folder='templates')

@redfin_api_home.route('/')
@redfin_api_home.route('/index')
def home():
    postman = "https://documenter.getpostman.com/view/28972003/2s9YC4TXma#intro"
    return redirect(postman)

@redfin_api_home.route('/get_recent_sales', methods=['GET'])
def get_recent_sales():
    #TODO Clean up API calls, they work but can be cleaner
    allowed_args = ['count', 'property_type', 'postal_code', 'state_prov', 'city', 'location']
    req_data = request.args
    params=[]
    sql = "SELECT * FROM sold_properties WHERE sold_date NOT NULL"

    if 'count' not in req_data.keys():
        count=10
    else:
        count = req_data['count']
    for arg, value in req_data.items(): 
        if arg not in allowed_args:
            return 'ERROR INVALID PARAMETER PLEASE SEE DOCS'
        elif arg != 'count':
            try:
                params.append((value))
            except ValueError:
                params.append(value)
            sql = sql + f' AND {arg} = (?)'

    sql = sql + " ORDER BY sold_year DESC, sold_month DESC, sold_day DESC LIMIT (?)"
    params.append(int(count))
    con = sqlite3.connect(DB_URL)
    df = pd.read_sql(sql, con, params=params,)
    con.close()
    if df.empty:
        return 'No data for these search parameters'
    df = df[['sold_date', 'property_type', 'address', 'city', 'state_prov', 'postal_code', 'location',
             'price', 'beds', 'baths', 'sqft', 'lot_size', 'year_built', 'hoa_monthly', 'url', 'mls', 'lat', 'lng']]

    return df.to_json(orient="records")

@redfin_api_home.route('/get_random_sales', methods=['GET'])
def get_random_sales():
    #TODO Clean up API calls, they work but can be cleaner
    allowed_args = ['count', 'property_type', 'postal_code', 'state_prov', 'city', 'location']
    req_data = request.args
    params=[]
    sql = "SELECT * FROM sold_properties WHERE lat NOT NULL"

    if 'count' not in req_data.keys():
        count=10
    else:
        count = req_data['count']
    for arg, value in req_data.items(): 
        if arg not in allowed_args:
            return 'ERROR INVALID PARAMETER PLEASE SEE DOCS'
        elif arg != 'count':
            try:
                params.append((value))
            except ValueError:
                params.append(value)
            sql = sql + f' AND {arg} = (?)'

    sql = sql + " ORDER BY RANDOM() LIMIT (?)"
    params.append(int(count))
    con = sqlite3.connect(DB_URL)
    df = pd.read_sql(sql, con, params=params,)
    con.close()
    if df.empty:
        return 'No data for these search parameters'
    df = df[['sold_date', 'property_type', 'address', 'city', 'state_prov', 'postal_code', 'location',
             'price', 'beds', 'baths', 'sqft', 'lot_size', 'year_built', 'hoa_monthly', 'url', 'mls', 'lat', 'lng']]

    return df.to_json(orient="records")

@redfin_api_home.route('/get_most_expensive', methods=['GET'])
def get_most_expensive():
    #TODO Clean up API calls, they work but can be cleaner
    allowed_args = ['count', 'property_type', 'postal_code', 'state_prov', 'city', 'location']
    req_data = request.args
    params=[]
    sql = "SELECT * FROM sold_properties WHERE price > 1000"

    if 'count' not in req_data.keys():
        count=10
    else:
        count = req_data['count']
    for arg, value in req_data.items(): 
        if arg not in allowed_args:
            return 'ERROR INVALID PARAMETER PLEASE SEE DOCS'
        elif arg != 'count':
            try:
                params.append((value))
            except ValueError:
                params.append(value)
            sql = sql + f' AND {arg} = (?)'

    sql = sql + " ORDER BY price DESC LIMIT (?)"
    params.append(int(count))
    con = sqlite3.connect(DB_URL)
    df = pd.read_sql(sql, con, params=params,)
    con.close()
    if df.empty:
        return 'No data for these search parameters'
    df = df[['sold_date', 'property_type', 'address', 'city', 'state_prov', 'postal_code', 'location',
             'price', 'beds', 'baths', 'sqft', 'lot_size', 'year_built', 'hoa_monthly', 'url', 'mls', 'lat', 'lng']]

    return df.to_json(orient="records")


@redfin_api_home.route('/get_least_expensive', methods=['GET'])
def get_least_expensive():
    #TODO Clean up API calls, they work but can be cleaner
    allowed_args = ['count', 'property_type', 'postal_code', 'state_prov', 'city', 'location']
    req_data = request.args
    params=[]
    sql = "SELECT * FROM sold_properties WHERE price > 1000"

    if 'count' not in req_data.keys():
        count=10
    else:
        count = req_data['count']
    for arg, value in req_data.items(): 
        if arg not in allowed_args:
            return 'ERROR INVALID PARAMETER PLEASE SEE DOCS'
        elif arg != 'count':
            try:
                params.append((value))
            except ValueError:
                params.append(value)
            sql = sql + f' AND {arg} = (?)'

    sql = sql + " ORDER BY price LIMIT (?)"
    params.append(int(count))
    con = sqlite3.connect(DB_URL)
    df = pd.read_sql(sql, con, params=params,)
    con.close()
    if df.empty:
        return 'No data for these search parameters'
    df = df[['sold_date', 'property_type', 'address', 'city', 'state_prov', 'postal_code', 'location',
             'price', 'beds', 'baths', 'sqft', 'lot_size', 'year_built', 'hoa_monthly', 'url', 'mls', 'lat', 'lng']]

    return df.to_json(orient="records")

@redfin_api_home.route('/get_most_baths', methods=['GET'])
def get_most_baths():
    #TODO Clean up API calls, they work but can be cleaner
    allowed_args = ['count', 'property_type', 'postal_code', 'state_prov', 'city', 'location']
    req_data = request.args
    params=[]
    sql = "SELECT * FROM sold_properties WHERE baths < 10 * beds"

    if 'count' not in req_data.keys():
        count=10
    else:
        count = req_data['count']
    for arg, value in req_data.items(): 
        if arg not in allowed_args:
            return 'ERROR INVALID PARAMETER PLEASE SEE DOCS'
        elif arg != 'count':
            try:
                params.append((value))
            except ValueError:
                params.append(value)
            sql = sql + f' AND {arg} = (?)'

    sql = sql + " ORDER BY baths DESC LIMIT (?)"
    params.append(int(count))
    con = sqlite3.connect(DB_URL)
    df = pd.read_sql(sql, con, params=params,)
    con.close()
    if df.empty:
        return 'No data for these search parameters'
    df = df[['sold_date', 'property_type', 'address', 'city', 'state_prov', 'postal_code', 'location',
             'price', 'beds', 'baths', 'sqft', 'lot_size', 'year_built', 'hoa_monthly', 'url', 'mls', 'lat', 'lng']]

    return df.to_json(orient="records")

@redfin_api_home.route('/get_most_beds', methods=['GET'])
def get_most_beds():
    #TODO Clean up API calls, they work but can be cleaner
    allowed_args = ['count', 'property_type', 'postal_code', 'state_prov', 'city', 'location']
    req_data = request.args
    params=[]
    sql = "SELECT * FROM sold_properties WHERE beds < 10 * baths"

    if 'count' not in req_data.keys():
        count=10
    else:
        count = req_data['count']
    for arg, value in req_data.items(): 
        if arg not in allowed_args:
            return 'ERROR INVALID PARAMETER PLEASE SEE DOCS'
        elif arg != 'count':
            try:
                params.append((value))
            except ValueError:
                params.append(value)
            sql = sql + f' AND {arg} = (?)'

    sql = sql + " ORDER BY beds DESC LIMIT (?)"
    params.append(int(count))
    con = sqlite3.connect(DB_URL)
    df = pd.read_sql(sql, con, params=params,)
    con.close()
    if df.empty:
        return 'No data for these search parameters'
    df = df[['sold_date', 'property_type', 'address', 'city', 'state_prov', 'postal_code', 'location',
             'price', 'beds', 'baths', 'sqft', 'lot_size', 'year_built', 'hoa_monthly', 'url', 'mls', 'lat', 'lng']]

    return df.to_json(orient="records")

@redfin_api_home.route('/get_most_sqft', methods=['GET'])
def get_most_sqft():
    #TODO Clean up API calls, they work but can be cleaner
    allowed_args = ['count', 'property_type', 'postal_code', 'state_prov', 'city', 'location']
    req_data = request.args
    params=[]
    sql = "SELECT * FROM sold_properties WHERE sqft < 10 * lot_size"

    if 'count' not in req_data.keys():
        count=10
    else:
        count = req_data['count']
    for arg, value in req_data.items(): 
        if arg not in allowed_args:
            return 'ERROR INVALID PARAMETER PLEASE SEE DOCS'
        elif arg != 'count':
            try:
                params.append((value))
            except ValueError:
                params.append(value)
            sql = sql + f' AND {arg} = (?)'

    sql = sql + " ORDER BY sqft DESC LIMIT (?)"
    params.append(int(count))
    con = sqlite3.connect(DB_URL)
    df = pd.read_sql(sql, con, params=params,)
    con.close()
    if df.empty:
        return 'No data for these search parameters'
    df = df[['sold_date', 'property_type', 'address', 'city', 'state_prov', 'postal_code', 'location',
             'price', 'beds', 'baths', 'sqft', 'lot_size', 'year_built', 'hoa_monthly', 'url', 'mls', 'lat', 'lng']]
    return df.to_json(orient="records")

@redfin_api_home.route('/get_high_ppsqft', methods=['GET'])
def get_high_ppsqft():
    #TODO Clean up API calls, they work but can be cleaner
    allowed_args = ['count', 'property_type', 'postal_code', 'state_prov', 'city', 'location']
    req_data = request.args
    params=[]
    sql = "SELECT * FROM sold_properties WHERE price_per_sqft NOT NULL AND sqft > 100"

    if 'count' not in req_data.keys():
        count=10
    else:
        count = req_data['count']
    for arg, value in req_data.items(): 
        if arg not in allowed_args:
            return 'ERROR INVALID PARAMETER PLEASE SEE DOCS'
        elif arg != 'count':
            try:
                params.append((value))
            except ValueError:
                params.append(value)
            sql = sql + f' AND {arg} = (?)'

    sql = sql + " ORDER BY price_per_sqft DESC LIMIT (?)"
    params.append(int(count))
    con = sqlite3.connect(DB_URL)
    df = pd.read_sql(sql, con, params=params,)
    con.close()
    if df.empty:
        return 'No data for these search parameters'
    df = df[['sold_date', 'property_type', 'address', 'city', 'state_prov', 'postal_code', 'location',
             'price', 'beds', 'baths', 'sqft', 'lot_size', 'year_built', 'price_per_sqft', 'hoa_monthly', 'url', 'mls', 'lat', 'lng']]
    return df.to_json(orient="records")