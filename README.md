# Craigslist Scraper


## NOTICE: Code Removed due to Cease and Desist

Craiglist sent us a Cease and Desist letter, forcing us to remove the code on this page. Fuck you Craiglist, you could have just asked nicely. It was just a class project. This isn't how we do things here. 

For those interested, here's the Cease and Desist letter: https://github.com/njoubert/CraigslistScraperVisualizer/raw/master/123575442_1.pdf

The code has been purged from this repository, and we are no longer in voilation of Craiglist's TOS. There's still some pretty images below. 

The lawyers in question is Perkins Coie LLP.

## Project Overview

This project scrapes Craigslist for housing posts, visualizes it as a brushing-and-linking interface between histograms and spatial layouts. This is a class project for Prof. Jeff Heer's CS448B class at Stanford. 


**Authors:**
 
- Niels Joubert [@njoubert](http://github.com/njoubert)
- Eric Schkufza [@eschkufz](https://github.com/eschkufz)

***Use at your own risk, we assume no liability, this was purely written as a technology demo for a class project***

![CLScraper Image](https://raw.github.com/njoubert/CraigslistScraperVisualizer/master/CLScraper_screenshot.png)


## Dirty Details

### Installation of the Visualization webapp

Please see /src/webserver/INSTALL for instructions on 
getting the webserver running

### Running Visualization App 

just launch ./webserver.sh

### Running the Craigslist scraper

this depends on a mysql database with the schema of /src/db/schema.sql
now you can run /src/scraper/scraper.py and it will poll craigslist and populate the database