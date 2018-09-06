from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
# from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.embed import components

app = Flask(__name__)

feature_names = ['AAPL','GOOG','INTC','KO','MSFT','T','HPQ','WMT']
# plotting the data
def create_figure(current_feature_name):
    #Grab data from quandl
    url_dataset = 'https://www.quandl.com/api/v3/datasets/WIKI/'
    url_options = '/data.json?start_date=2018-01-01&end_date=2018-01-31&order=asc&column_index=4&api_key=VmrejGLj7UAexzD_wssd'  # only retrieve Jan 2018
    api_url = url_dataset + current_feature_name + url_options
    session = requests.Session()
    raw_data = session.get(api_url)
    data = raw_data.json()['dataset_data']
    df = pd.DataFrame(data['data'], columns=['Date', 'Closing'])

    #Create a line plot
    df['Date'] = pd.to_datetime(df['Date'])
    source = ColumnDataSource(df)
    p = figure(title='Quandl WIKI Closing Stock Prices - Jan 2018', plot_width=500, plot_height=500,
               x_axis_type='datetime')
    p.line('Date', 'Closing', source=source, legend=current_feature_name, line_width=2)
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    return p


@app.route('/')
def ClosingPrices():
    current_feature_name = request.args.get("feature_name")
    if current_feature_name == None:
        current_feature_name = "GOOG"

    #Create a plot
    plot = create_figure(current_feature_name)
    #Embed plot into HTML
    script, div = components(plot)
    return render_template('ClosingPrices.html', script=script, div=div, feature_names=feature_names, current_feature_name=current_feature_name)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(port=33507)