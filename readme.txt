JSON Object returned by /year-info route:

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