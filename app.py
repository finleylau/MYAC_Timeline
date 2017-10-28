from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from json import load
from flask_jsglue import JSGlue

# configure app
app = Flask(__name__,static_url_path="")
JSGlue(app)

# database file
db_file = "db.json"

# app routes
@app.route("/")
@app.route("/home")
def home():
    """Renders the home page."""
    return render_template("home.html")

@app.route("/events")
def events():
    """ Returns json object of timeline data """

    """
    JSON Object Format:
    {
        "<<year_id>>" : {
            "events": [
                {
                    "day": <<day>>,
                    "description": <<description>>,
                    "image_path": <<image_path>>,
                    "link": <<link>>,
                    "media_path": <<media_path>>,
                    "month": <<month>>,
                    "name": <<name>>
                }
                ...
                ],
            "people": {
                "admin": [],
                "artistic": [],
                "board": []
                }
            "year_info": {
                "end_year": <<end_year>>,
                "start_year": <<start_year>>
                }
        },
        ...
    }
    """
    json_data = open(db_file)
    data = load(json_data)

    return jsonify(data)

@app.route("/timeline")
def timeline():
    """Renders timeline page."""
    return render_template("timeline.html")

@app.route("/contribute")
def contribute():
    """Renders contribute page."""
    return render_template("contribute.html")

@app.route("/error")
def error():
    """Renders no js page."""
    return render_template("nojs.html")

# run the app
if __name__ == "__main__":
    app.run()
