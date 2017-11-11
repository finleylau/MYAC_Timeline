from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import FileUploadField
from wtforms.validators import InputRequired
from wtforms.fields import SelectField
import os
from database import Years, People


"""
TODO
-Store files in AWS S3 using Flask extensions
-Admin homepage
"""

mediapath = "static/media/events/"
imagepath = "static/img/event_pictures/"

def convert_yearid(view, context, model, name):
	year_id = getattr(model,name)
	return (1992+year_id)

def convert_typeid(view, context, model, name):
	type_id = getattr(model,name)
	if type_id == 1:
		return("Board")
	elif type_id == 2:
		return("Artistic")
	elif type_id == 3:
		return("Admin")
	else:
		print("Error in converting type_id")


class FileCustomUpload(FileUploadField):
	allowed_extensions = ["pdf", "jpeg", "jpg", "png"]

class PeopleView(ModelView):
	column_list = ["name", "type_id", "year_id"]
	column_searchable_list = ["name", "year_id"]
	column_labels = dict(
		name="Name",
		type_id="Type",
		year_id="Year")
	column_formatters = dict(
		type_id=convert_typeid,
		year_id=convert_yearid)

	form_columns = ["name","type_id","year_id"]
	form_overrides = dict(
		type_id = SelectField)
	
	form_args = dict(
		name= dict (label="Person Name", validators=[InputRequired()]),
		type_id = dict(label="Department", validators=[InputRequired()], choices=[("1","Board of Directors"), ("2", "Artistic Faculty"), ("3", "Administrative Staff")]),
		year_id = dict(label="Year to Display Person", validators=[InputRequired()]))

	def on_model_change(self, form, model):
		if int(model.year_id) >= 1993:
			model.year_id = model.year_id - 1992

		type_id = int(form.type_id.data)
		model.type_id = type_id

		self.session.commit()


class YearsView(ModelView):
	can_edit = False
	can_delete = True
	column_list =  ["start_year"]
	column_labels = dict(
		start_year = "Year Name")

	form_args = dict(
		start_year = dict(label="Year Name", default="This value will be created automatically when you submit this form"))

	form_widget_args = dict(
		start_year = dict(
			readonly = True))

	def create_model(self,form):

		previous_year = self.session.query(Years).order_by(Years.year_id.desc()).first()
		new_year = Years()
		previous_year_id = previous_year.year_id
		new_year.start_year = str(previous_year_id + 1993)
		new_year.year_id = int(new_year.start_year) - 1992

		self.session.add(new_year)
		self.session.commit()

		added_year = self.session.query(Years).order_by(Years.year_id.desc()).first()
		added_year_id = added_year.year_id

		year_id_for_query = (int(new_year.start_year)-1) - 1992 
		people = People.query.filter_by(year_id = year_id_for_query).all()

		for person in people:
			new_person = People()
			self.session.add(new_person)
			self.session.flush()

			added_person = People.query.order_by(People.person_id.desc()).first()

			added_person.type_id = person.type_id
			added_person.year_id = added_year_id
			added_person.name = person.name

			self.session.flush()

		self.session.commit()

		return True
		
		# BUG: PEOPLE AREN'T DISPLAYING BECAUSE OF IMPLEMENTATION OF HELPER FUNCTIONS

class EventsView(ModelView):
	column_list = ["name","month","day","year_id","description","link","image","media"]
	column_searchable_list = ["name"]
	column_labels = dict(name="Event Name", month="Month (number)", day="Day (number)",
		year_id="Start Year", description="Event Description", link="Event Video Link",
		image="Image", media="Media")
	column_formatters = dict(
		year_id=convert_yearid)

	form_columns = ["name","month","day","year_id","description","link","image","media"]
	form_overrides = dict(
		image=FileCustomUpload,
		media=FileCustomUpload)

	form_args = dict(
		name=dict(label="Event Name", validators=[InputRequired()]),
		month=dict(label="Month (number)", validators=[InputRequired()]),
		day=dict(label="Day (number)", validators=[InputRequired()]),
		year_id=dict(label="Start Year", validators=[InputRequired()]),
		description=dict(label="Event Description"),
		link=dict(label="Event Video Link"),
		image=dict(label="Event Image Upload", base_path=imagepath),
		media=dict(label="Event Media Upload", base_path=mediapath))

	def after_model_change(self, form, model, is_created):
		
		if int(model.year_id) >= 1993:
			model.year_id = model.year_id - 1992

		if model.description is None or model.description == "":
			model.description = "None"

		if model.link is None or model.link == "":
			model.link = "None"

		if is_created:
			if form.image.data is not None:
				image_name = form.image.data.filename
				ext = ""
				if '.' in image_name and image_name.rsplit('.',1)[1] in ["jpg", "jpeg", "png"]:
					if image_name.rsplit('.',1)[1] == "jpg":
						ext = ".jpg"
					elif image_name.rsplit('.',1)[1] == "jpeg":
						ext = ".jpeg"
					else:
						ext = ".png"

					filename = str(model.event_id) + ext
					
					if os.path.exists(imagepath + image_name):
						os.remove(imagepath + image_name)

					if os.path.exists(imagepath+filename):
						os.remove(imagepath + filename)
						form.image.data.save(imagepath + filename)
					else:
						form.image.data.save(imagepath + filename)

					model.image = filename

			if form.media.data is not None:
				media_name = form.media.data.filename
				ext = ".pdf"
				if '.' in media_name and media_name.rsplit('.',1)[1] in ["pdf"]:
					
					filename = str(model.event_id) + ext
					
					if os.path.exists(mediapath + media_name):
						os.remove(mediapath + media_name)

					if os.path.exists(mediapath+filename):
						os.remove(mediapath + filename)
						form.media.data.save(mediapath + filename)
					else:
						form.media.data.save(mediapath + filename)


					model.media = filename
		else:
			if form.image.data is not None:
				if hasattr(form.image.data, "filename"):
					image_name = form.image.data.filename
					ext = ""
					if '.' in image_name and image_name.rsplit('.',1)[1] in ["jpg", "jpeg", "png"]:
						if image_name.rsplit('.',1)[1] == "jpg":
							ext = ".jpg"
						elif image_name.rsplit('.',1)[1] == "jpeg":
							ext = ".jpeg"
						else:
							ext = ".png"

						filename = str(model.event_id) + ext
						
						if os.path.exists(imagepath + image_name):
							os.remove(imagepath + image_name)

						if os.path.exists(imagepath+filename):
							os.remove(imagepath + filename)
							form.image.data.save(imagepath + filename)
						else:
							form.image.data.save(imagepath + filename)

						model.image = filename

			if form.media.data is not None:
				if hasattr(form.media.data, "filename"):
					media_name = form.media.data.filename
					ext = ".pdf"
					if '.' in media_name and media_name.rsplit('.',1)[1] in ["pdf"]:
						
						filename = str(model.event_id) + ext
						
						if os.path.exists(mediapath + media_name):
							os.remove(mediapath + media_name)

						if os.path.exists(mediapath+filename):
							os.remove(mediapath + filename)
							form.media.data.save(mediapath + filename)
						else:
							form.media.data.save(mediapath + filename)



		if model.image is None or model.image == "":
			model.image = "None"

		if model.media is None or model.media == "":
			model.media = "None"

		self.session.commit()
		return True
