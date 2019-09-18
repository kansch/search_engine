# Search engine

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

`
mkvirtualenv search_engine --python=/usr/bin/python3.6
pip install -r requirements.txt
`
