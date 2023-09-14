from flask import Flask, render_template
import pandas as pd
import numpy as np
app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations.drop(columns=['      LAT','       LON','HGHT', 'CN'])

@app.route("/")
def home():
    return render_template("home.html", station_data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    temperature = 23
    dataframe = pd.read_csv(f"data_small/TG_STAID{str(station).zfill(6)}.txt", skiprows=20, parse_dates=["    DATE"])
    dataframe['TG0'] = dataframe['   TG'].mask(dataframe['   TG'] == -9999, np.nan)
    dataframe['TG'] = dataframe['TG0'] / 10
    temperature = dataframe.loc[dataframe['    DATE'] == date]['TG'].squeeze()
    return {"station": station,
            "date": date,
            "temperature": temperature}

if __name__ == "__main__":
    app.run(debug=True, port=5000)