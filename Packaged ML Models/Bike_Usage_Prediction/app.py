from flask import Flask, request, abort
import argparse
import sklearn
import sys
import ie_bike_model
from ie_bike_model.model import train_and_persist as train, predict as pred
import datetime as dt
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def versions():
    return {
        "python-version": sys.version[0:5],
        "scikit-learn-version": sklearn.__version__,
        "ie_bike_model-version": ie_bike_model.__version__,
    }


@app.route("/train_and_persist")
def train_and_persist():
    if train() == None:
        return {
            "status": "ok",
        }
    else:
        abort(400)


@app.route("/predict")
def predict():
    args = dict(request.args)
    try:
        dict_param = {
            "date": datetime.strptime(args.get("date"), "%Y-%m-%dT%H:%M:%S"),
            "weathersit": int(args.get("weathersit")),
            "temperature_C": float(args.get("temperature_C")),
            "feeling_temperature_C": float(args.get("feeling_temperature_C")),
            "humidity": float(args.get("humidity")),
            "windspeed": float(args.get("windspeed")),
        }
        begin_time = dt.datetime.now()
        result = pred(dict_param)
        exec_time = dt.datetime.now() - begin_time
        secs = exec_time.total_seconds()
        return {"result": result, "elapsed_time": str(secs)}
    except:
        abort(400)


if __name__ == "__main__":
    # Use python app.py --help to showcase argument parsing
    parser = argparse.ArgumentParser(description="Bike Usage Prediction App")
    parser.add_argument("--debug_off", action="store_false", help="Disable debug mode")
    args = parser.parse_args()

    app.run(debug=args.debug_off)
