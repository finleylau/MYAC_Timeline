from flask_wtf import FlaskForm
from wtforms import validators, ValidationError
from wtforms.fields import TextField, SelectField, TextAreaField, IntegerField, SubmitField, DateField, PasswordField
from flask_wtf.file import FileField
from database import Users
from werkzeug.security import check_password_hash

class ContactForm(FlaskForm):
	name = TextField("Your Name", [validators.InputRequired("Please enter your name!")])
	email = TextField("Email", [validators.InputRequired("Please enter your email!"), validators.Email("Please enter a valid email!")])
	eventname = TextField("Event Name", [validators.InputRequired("Please enter the event name!")])
	date = TextField("Date",[validators.InputRequired("Please enter the event date!")])
	description = TextAreaField("Event Description")
	image = FileField("Event image - .jpg, .png")
	media = FileField("Event media - .pdf")
	link = TextField("Video link")
	submit = SubmitField("Submit")

class LoginForm(FlaskForm):
	login = TextField(validators=[validators.required()])
	password = PasswordField(validators=[validators.required()])

	def validate_login(self, field):
		user = self.get_user()

		if user is None:
			raise validators.ValidationError('Invalid user')

		# we're comparing the plaintext pw with the the hash from the db
		if not check_password_hash(user.password, self.password.data):
		# to compare plain text passwords use
		# if user.password != self.password.data:
			raise validators.ValidationError('Invalid password')

	def get_user(self):
		return Users.query.filter_by(login=self.login.data).first()