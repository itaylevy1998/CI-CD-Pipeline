# Reviewed By: Saveliy
from flask import Flask, render_template, request, abort
import requests
from dotenv import load_dotenv
import os


app = Flask(__name__)


@app.errorhandler(500)
def internal_error(error):
    """"Handles 500 error codes"""
    return "500 error"

@app.route('/')
def home():
    print("hello world!!")
    """"Handles home domain GET requests"""
    return render_template('home.html', message=None)

@app.route('/get_weather')
def forecast():
    """This endpoint launches 2 API requests, one for country and one for the weather"""
    print("hello!")
    city = request.args.get('city', "")
    # my_key = "SUWK9ET8MFNECXY3SCNQK464H"
    load_dotenv()
    my_key = os.getenv("API_KEY")
    weather_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/next6days?unitGroup=metric&elements=datetime%2CdatetimeEpoch%2Cname%2Caddress%2Clatitude%2Clongitude%2Ctempmax%2Ctempmin%2Ctemp%2Chumidity&include=days&key={my_key}&contentType=json"
    country_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&format=json"
    try:
        # country API
        country_response = requests.get(country_url)
        country_json = country_response.json()
        if country_json.get("results") is None or country_response.status_code != 200:
            return render_template('home.html', message=f"No such city: {city}")

        # weather API
        weather_response = requests.get(weather_url)
        if weather_response.status_code != 200:
            return render_template('home.html', message=f"No such city: {city}")

        country = country_json["results"][0]["country"]
        weather_json = weather_response.json()
        days_list = weather_json["days"]
    except Exception as e:
        abort(500)
    return render_template('forecast_display.html', data=days_list, location=city, country=country)


if __name__ == "__main__":
    """Run server"""
    app.run(host='0.0.0.0', port=3000, debug=True)


