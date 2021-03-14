# Analysis with SQLAlchemy
### Climate Analysis and Exploration
Performed Climate Analysis and data exploration using `Python` and `SQLAlchemy` ORM queries using a [hawaii.sqlite](Resources/hawaii.sqlite) file.

#### Precipitation Analysis
Query the last 12 Months of Precipitation data and generated a line Plot of the results.

<img src="plots/Precipitation.png" alt="Precipitation Plot"/>
 
#### Station Analysis
Performed the following queries to obtain more detail information about the dataset:
* Query the total number of stations in the dataset
* Query the most active stations
* Query station with the highest number of observations
* Query the lowest, highest and average temperature for the most active station.
* Histogram Plot with the temperature observations in the last 12 months.

<img src="plots/station_tobs.png" alt="Station TOBS"/>

#### Climate App
Designed a `Flask` API based on previous developed queries. Used Flask `jsonify` to convert the API data into a valid JSON response object.

For this app several routes where created:

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Return a JSON representation of the precipitation values from the dataset.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`

  * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum, average and max temperature for a given start or start-end range date.

