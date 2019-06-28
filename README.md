# Tigertales

[Tigertales](https://tigertales.herokuapp.com ) is a textbook marketplace and exchange hub for Princeton students. Receive email notifications immediately to connect you to sellers when the books you're searching for become available; filter by book name, course code, and more; compare prices to the market value scraped from Amazon and local book stores.

## Dependencies and Requirements

Django 2.0.5
Python 2.7.14

Please see the requirements.txt for additional dependencies. 

### Local Development

For development team: once your Django virtual environment is set up, configure the database settings (in tigertales/settings.py) to point to a database modeled after the SQL dump (tigertales/dump.sql). Run from a local server by running the following commands:

```
cd tigertales
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in a browser and enter login information to explore the application. 


## Functionality

</br>
<p align="center">

<img src="resources/landing.png" width = "825px" />

<img src="resources/function.png" width = "825px" />

</p>

## Acknowledgments

Contributors: Colton Bishop, Sonia Hashim, Morlan Osgood, Annette Chu, Ben Yap, 

This project was advised by Professor Brian Kernighan.
