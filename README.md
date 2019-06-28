# Tigertales

[Tigertales](https://tigertales.herokuapp.com ) is a textbook marketplace and exchange hub for Princeton students. Receive email notifications immediately to connect you to sellers when the books you're searching for become available; filter by book name, course code, and more; compare prices to the market value scraped from Amazon and local book stores.

## Dependencies and Requirements

Django 2.0.5
Python 2.7.14

Please see the requirements.txt for additional dependencies. 

### Run from local machine

Once your Django virtual environment is set up, edit the database settings (in tigertales/settings.py) to point to a dummy database modeled after the SQL dump (tigertales/dump.sql). Run a local copy of the app by running the following commands:

```
cd tigertales
python manage.py runserver
```

</br>
<p align="center">

<img src="resources/landing.png" width = "825px" />

<img src="resources/function.png" width = "825px" />

</p>

## Acknowledgments

Contributors: Colton Bishop, Sonia Hashim, Morlan Osgood, Annette Chu, Ben Yap, 

This project was advised by Professor Brian Kernighan.
