from django import forms
from django.forms.formsets import BaseFormSet
from django.forms import ModelForm
from .models import Course, Book

class ProfileForm(forms.Form):
	first_name = forms.CharField(label='First Name', max_length=100, required=False)
	last_name = forms.CharField(label='Last Name', max_length=100, required=False)
	venmo = forms.CharField(label='Venmo', max_length=100, required=False)
	facebook = forms.CharField(label='Facebook', max_length=100, required=False)
	email = forms.CharField(label='Preferred Email', max_length=100, required=False)
	courses = forms.CharField(label='Courses', max_length=250, required=False)

class SearchForm(forms.Form):
	search = forms.CharField(label='Search', max_length=250, required=False)

class RequestForm(forms.Form):
	offer_price = forms.CharField(label='Offer Price', max_length=100, required=False)
	formID = forms.CharField(label='Offer Price', max_length=100, required=False)

class NewRequestForm(forms.Form):
	offer_price = forms.CharField(label='', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g. $10, late meal, a hug'}))
	fav_id = forms.CharField(widget = forms.HiddenInput(), required = False)

class ListingForm(forms.Form):
	book = forms.CharField(label='Book', max_length=500, required=True, widget=forms.TextInput(attrs={'placeholder': 'e.g. Kingdon Pocket Guide, African Mammals'}))
	price = forms.CharField(label='Price', max_length=500, required=True, widget=forms.TextInput(attrs={'placeholder': 'e.g. $5, snacks, free'}))
	condition = forms.CharField(label='Condition', max_length=500, required=True, widget=forms.TextInput(attrs={'placeholder': 'e.g. Like-new (dog-eared corners), Used (highlights)'}))
