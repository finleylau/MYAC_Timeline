from flask_wtf import Form
from wtforms import validators, ValidationError
from wtforms.fields import TextField, TextAreaField, SubmitField, DateField
from flask_wtf.file import FileField

class ContactForm(Form):
  name = TextField("Your Name", [validators.InputRequired("Please enter your name!")])
  email = TextField("Email", [validators.InputRequired("Please enter your email!"), validators.Email("Please enter a valid email!")])
  eventname = TextField("Event Name", [validators.InputRequired("Please enter the event name!")])
  date = TextField("Date",[validators.InputRequired("Please enter the event date!")])
  description = TextAreaField("Event Description")
  image = FileField("Event image - .jpg, .png")
  media = FileField("Event media - .pdf")
  link = TextField("Video link")
  submit = SubmitField("Submit")