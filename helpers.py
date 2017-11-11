""" Helper functions for main app """


# creates list of years
def get_years(database_years):
	years = []
	for i in database_years:
		year = {}
		year["start_year"] = int(i.start_year)
		year["end_year"] = year["start_year"] + 1
		year["year_id"] = int(i.start_year) - 1992
		years.append(year)

	return years

# creates list of people
def get_people(num_years, database_people):
	people_by_year = [None] * num_years
	for i in range(num_years):
		people_by_year[i] = {"admin":[],"artistic":[],"board":[]}

	for i in database_people:
		person_year_id = i.year_id
		try:
			if i.type_id == 1:
				people_by_year[person_year_id-1]["board"].append(i.name)
			elif i.type_id == 2:
				people_by_year[person_year_id-1]["artistic"].append(i.name)
			elif i.type_id == 3:
				people_by_year[person_year_id-1]["admin"].append(i.name)
		except:
			pass

	return people_by_year

# creates list of events
def get_events(num_years, database_events):
	events_by_year = [None] * num_years
	for i in range(num_years):
		events_by_year[i] = []

	for i in database_events:
		event_year = i.year_id
		try:
			event = {}
			event_year = i.year_id

			event["name"] = i.name
			event["month"] = str(i.month)
			event["day"] = str(i.day)
			if i.description is not None:
				event["description"] = i.description
			else:
				event["description"] = "None"

			# build file paths
			if i.image == "None" or i.image is None:
				event["image_path"] = ""
			else:
				event["image_path"] = "img/event_pictures/" + i.image

			if i.media == "None" or i.media is None:
				event["media_path"] = ""
			else:
				event["media_path"] = "media/events/" + i.media

			if i.link == "None" or i.link is None:
				event["link"] = ""
			else:
				event["link"] = i.link

			events_by_year[event_year-1].append(event)
		except:
			pass

	# sorts events by month and day
	sorted_events_by_year = []

	for i in events_by_year:
		events = sorted(i, key=lambda k: (int(k["month"]),int(k["day"])))
		second_half = []
		sorted_events = []

		# sorts events by school year calendar
		for event in events:
			if int(event["month"]) < 6:
				second_half.append(event)
			else:
				sorted_events.append(event)
		for event in second_half:
			sorted_events.append(event)

		sorted_events_by_year.append(sorted_events)

	return sorted_events_by_year