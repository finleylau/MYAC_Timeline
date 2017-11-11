from flask_wtf import Form
from wtforms import validators, ValidationError
from wtforms.fields import TextField, SelectField, TextAreaField, IntegerField, SubmitField, DateField
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


class AddYearForm(Form):
	start = IntegerField("Year's Start Year*", [validators.InputRequired("Please enter a year!")])
	submit = SubmitField("Add Year")

class AddPeopleForm(Form):
	name = TextField("Person Name*", [validators.InputRequired("Please input a person's name!")])
	person_year = IntegerField("Year*", [validators.InputRequired("Please enter what year this person was a part of the organization!")])
	person_type = SelectField(u'Person Type', choices = [("board", "Board of Directors"), ("artistic", "Artistic Faculty"), ("admin", "Administrative Staff")])
	submit = SubmitField("Add Person")

class AddEventsForm(Form):
	event_name = TextField("Event Name*", [validators.InputRequired("Please enter an event name")])
	month = IntegerField("Month (number)*", [validators.InputRequired("Please enter a month (number)")])
	day = IntegerField("Day (number)*", [validators.InputRequired("Please enter a day (number)")])
	event_year = IntegerField("Year*", [validators.InputRequired("Please enter a valid year")])
	event_description = TextField("Description")
	event_link = TextField("Link")
	event_image = FileField("Event image - .jpg, .png")
	event_media = FileField("Event media - .pdf")
	submit = SubmitField("Add Event")