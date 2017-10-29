from flask import Flask, flash, redirect, render_template, request, url_for, jsonify, flash
from json import load
from flask_jsglue import JSGlue
from forms import ContactForm
from flask_mail import Message, Mail
from werkzeug.utils import secure_filename
import os

# configure app
app = Flask(__name__,static_url_path="")
JSGlue(app)

app.secret_key = "s3d6Y0i9tMTuEKmy7FTi"

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "myactimeline@gmail.com"
app.config["MAIL_PASSWORD"] = "myactimeline12345"
mail = Mail(app)

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

@app.route("/contribute", methods=["GET","POST"])
def contribute():
    """Renders contribute page."""
    form = ContactForm()

    if request.method == "POST":
        if form.validate() == False:
            flash("Please make sure you've filled out your name, a valid email, the event name, and the event date.")
            return render_template("contribute.html", form=form)
        else:
            IMAGE_FILE_TYPES = set(['jpg', 'jpeg', 'png'])
            MEDIA_FILE_TYPES = set(['pdf'])
            msg = Message("MYAC Timeline Contact Email - New Event Request", sender='myactimeline@gmail.com', recipients=["finleylau@mya.org"])
            msg.body = "A new event request has been made from %s (%s).\n\nEvent Name: %s\nEvent Date: %s\nEvent Description: %s\nEvent Link: %s" % (form.name.data, form.email.data, form.eventname.data, form.date.data, form.description.data, form.link.data)

            if form.image.data != None:
                image_name = form.image.data.filename
                if '.' in image_name and image_name.rsplit('.', 1)[1] in IMAGE_FILE_TYPES:
                    if image_name.rsplit('.',1)[1] == "png":
                        contenttype = "image/png"
                    elif image_name.rsplit('.',1)[1] == "jpg" or image_name.rsplit('.',1)[1] == "jpeg":
                        contenttype = "image/jpeg"

                    filename = secure_filename(image_name)
                    form.image.data.save(filename)
                    with app.open_resource(filename) as fp:
                        msg.attach(filename = filename, content_type = contenttype, data = fp.read())
                    os.remove(filename)

            if form.image.data != None:
                media_name = form.media.data.filename
                if '.' in media_name and media_name.rsplit('.', 1)[1] in MEDIA_FILE_TYPES:
                    filename = secure_filename(media_name)
                    form.media.data.save(filename)
                    with app.open_resource(filename) as fp:
                        msg.attach(filename, "application/pdf", fp.read())
                    os.remove(filename)

            mail.send(msg)

            return render_template("contribute.html", success=True)

    elif request.method == "GET":
        return render_template("contribute.html", form=form)

@app.route("/error")
def error():
    """Renders no js page."""
    return render_template("nojs.html")

# run the app
if __name__ == "__main__":
    app.run()
