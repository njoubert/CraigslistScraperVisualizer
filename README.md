This scrapes Craigslist and visualizes Housing results on a map and as a set of histograms.

Use at your own risk, we assume no liability, this was purely written as a technology demo for a class project.

## Installation of the Visualization webapp

Please see /src/webserver/INSTALL for instructions on 
getting the webserver running

## Running Visualization App 

just launch ./webserver.sh

## Running the Craigslist scraper

this depends on a mysql database with the schema of /src/db/schema.sql
now you can run /src/scraper/scraper.py and it will poll craigslist and populate the database