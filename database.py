from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# create years table
class Years(db.Model):
	year_id = db.Column(db.Integer, primary_key = True)
	start_year = db.Column(db.Text, unique = True)

	def __init__(self, start_year=""):
		self.start_year = start_year

	def __repr__(self):
		return "<Years %r" % self.start_year

# create events table
class Events(db.Model):
	event_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
	year_id = db.Column(db.Integer)
	month = db.Column(db.Integer)
	day = db.Column(db.Integer)
	name = db.Column(db.Text)
	description = db.Column(db.Text)
	image = db.Column(db.Text)
	link = db.Column(db.Text)
	media = db.Column(db.Text)

	def __init__(self, year_id="", month="", day="", name="", description="", image="", link="", media=""):
		self.year_id = year_id
		self.month = month
		self.day = day
		self.name = name
		self.description = description
		self.image = image
		self.link = link
		self.media = media

	def __repr__(self):
		return "<Events %r" % self.name


# create People table
class People(db.Model):
	person_id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.Text)
	type_id = db.Column(db.Integer)
	year_id = db.Column(db.Integer)

	def __init__(self, name="", type_id=0, year_id=0):
		self.name = name
		self.type_id = type_id
		self.year_id = year_id

	def __repr__(self):
		return "<People %r" % str(self.person_id)


# create Types table
class Types(db.Model):
	type_id = db.Column(db.Integer, primary_key = True)
	type_name = db.Column(db.Text)

	def __init__(self, type_name):
		self.type_name = type_name

	def __repr__(self):
		return "<Types %r" & self.type_name