from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507)

  
import requests
import pandas as pd
from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

output_file("lines.html")

url_dataset = 'https://www.quandl.com/api/v3/datasets/WIKI/'
url_ticker = input("Ticker symbol ")
url_options = '/data.json?start_date=2018-01-01&end_date=2018-01-31&order=asc&column_index=4&api_key=VmrejGLj7UAexzD_wssd'#only retrieve Jan 2018

api_url = url_dataset + url_ticker + url_options
session = requests.Session()
raw_data = session.get(api_url)

if raw_data.status_code != 200:
    print ("Error. Please check your input...")
	
data = raw_data.json()['dataset_data']
df = pd.DataFrame(data['data'], columns=['Date','Closing'])
#plotting the data
df['Date'] = pd.to_datetime(df['Date'])
source = ColumnDataSource(df)

p = figure(title = 'Quandl WIKI Closing Stock Prices - Jan 2018', plot_width=500, plot_height=500, x_axis_type='datetime')
p.line('Date', 'Closing', source = source, legend = url_ticker, line_width=2)

show(p)