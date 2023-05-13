from flask import Flask, render_template, request
import requests
import pytz
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    response = requests.get('https://restcountries.com/v3.1/all')
    countries = response.json()
    country_list = [(country['name']['common'], country['cca2']) for country in countries]
    return render_template('index.html', country_list=country_list)

@app.route('/get_time', methods=['POST'])
def get_time():
    country_code = request.form['country']
    response = requests.get(f'https://restcountries.com/v3.1/alpha/{country_code}')
    country_data = response.json()

    # Check if the response is a list and get the first element
    if isinstance(country_data, list):
        country_data = country_data[0]

    timezones = country_data['timezones']
    if isinstance(timezones, list):
        timezone = timezones[0]
    else:
        timezone = timezones

    # Convert UTC offset to timezone name
    if timezone.startswith('UTC'):
        hours = int(timezone[4:].split(':')[0])
        minutes = int(timezone[4:].split(':')[1])
        tz = pytz.FixedOffset(hours * 60 + minutes)
    else:
        tz = pytz.timezone(timezone)

    current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    return {'time': current_time}

if __name__ == '__main__':
    app.run(debug=True)