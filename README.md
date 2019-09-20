# Search engine

A quick search engine with GIS filter. For demo purposes a ready to use spatialite database is provided.

## Required packages

* python 3.6
* virtualenv
* virtualenvwrapper
* gdal-bin
* libspatialite7
* libsqlite3-mod-spatialite

## Installation

Tested on Ubuntu 16.04 LTS

Clone this repo and cd into it.

`cd /your/home/path/search_engine`

Then create the virtualenv.

```
mkvirtualenv search_engine --python=/usr/bin/python3.6
pip install -r requirements.txt
```

Then you can run the server

`
python manage.py runserver
`

And use the API

```
curl "http://127.0.0.1:8000/api/campers/[?location=lon,lat&start_date=YYY-MM-DD&end_date=YYY-MM-DD]" -v
```

You have a root view of the API by visiting `http://127.0.0.1:8000/api/`

## Testing

A ``tox.ini`` file is provided:

```
pip install tox
tox
```

An HTML coverage report is also generated:

```
xdg-open htmlcov/index.html
```
