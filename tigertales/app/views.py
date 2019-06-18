# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta, datetime

from django.shortcuts import render
from .models import Book
from .models import Notifications

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# import CASClient
from django.contrib.auth.decorators import login_required
from django_cas_ng import views as casviews
from django.conf import settings

#import email functionality
from django.core.mail import send_mail
from django.template import loader

# MODELS
from .models import Listing, Book, Cart, Request, CourseList, Course, User

# FORMS
from django import forms
from django.forms import formset_factory
from .forms import ProfileForm, SearchForm, RequestForm, ListingForm, NewRequestForm
from copy import deepcopy

# Views

# Login (wrapper for django-cas-ng)
# Redirects to /app/ (see tigertales/settings.py)
def login(request, **kwargs):
	return casviews.login(request, **kwargs)

# Logout (wrapper for django-cas-ng)
# No redirect at the moment
def logout(request, **kwargs):
	return casviews.logout(request, **kwargs)

# Landing
def index(request):
	context = {}
	# If authenticated, redirect to profile or main listings page
	if request.user.is_authenticated:
		print "user is authenticated"
		# If it's the first login, redirect to profile page
		threshold = timedelta(days = 0, minutes = 0, seconds = 15)
		if (timezone.now() - request.user.date_joined) < threshold:
			print ("first login")
			return HttpResponseRedirect(reverse('app:profile'))
		context['netid'] = request.user
		# Otherwise (not first login), redirect to main page
		return HttpResponseRedirect(reverse('app:main'))
	# Otherwise (not authenticated), return to landing
	return render(request, 'app/landing', context)

## AUTH PROTECTED

@login_required
# Shows all listings, note dummy argument to process adding listing to cart
def main(request, id=-1):
	user = request.user.user
	net_id = user.net_id
	listings = Listing.objects.all()
	err_msg = ''
	saved_listing = ''
	show_modal = 'false'
	# Search bar form handling
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			clean = form.cleaned_data
			search_query = clean.get('search')
			# Maybe add some logic here to match courses, isbn, or titles
			listings = Listing.objects.filter(book__title__icontains = search_query)
			courses = Course.objects.filter(course_name__icontains = search_query)
			for c in courses:
				books = Book.objects.filter(course = c)
				for book in books:
					book_listings = Listing.objects.filter(book = book)
					listings = listings | book_listings
			if not hasattr(listings, '__iter__'):
				listings = [listings]
	# If there is a numeric arg, process request to add listing to cart
	if id>0:
		try:
			listing = Listing.objects.get(id=id)
			print listing
			# Avoid the user re-adding the listing to their cart
			if not Cart.objects.filter(listing=listing, user= user).exists():
				favorite = Cart.objects.create(
					listing = listing,
					user = user
				)
				print favorite
				saved_listing = favorite.listing.book.title
			else:
				err_msg = 'We\'ve already saved this listing to your favorites!'
		except:
			err_msg = 'Sorry, we couldn\'t add your listing to the exchange.'
		show_modal = 'true'
	form = SearchForm()

	context = {
		'net_id': net_id,
		'listings': listings,
		'form': form,
		'first_name': user.first_name,
		'last_name': user.last_name,
		'err_msg': err_msg,
		'saved_listing': saved_listing,
		'show_modal': show_modal # Note: this must be 'true' or 'false'
	}
	return render(request, 'app/main', context)

@login_required
def cart(request,id=-1):
	user = request.user.user
	msg = ''
	err_msg = ''
	show_modal = 'false'
	favorites = Cart.objects.filter(user = user)
	RequestFormset = formset_factory(NewRequestForm, extra = len(favorites))
	formset = RequestFormset()

	# Process formset with price offers to make a request or delete the item
	if request.method == 'POST':
		formset = RequestFormset(request.POST)
		if formset.is_valid():
			# Iterate through the form for each listing
			for i, f in enumerate(formset):
				clean = f.cleaned_data
				offer_price = clean.get('offer_price')
				fav_id = clean.get('fav_id')
				# If the value has changed, make a request
				if offer_price and 'request' in request.POST:
					print 'making a request'
					print fav_id
					fav = Cart.objects.filter(id=fav_id)
					if fav.exists():
						print 'ok this thing exists'
						listing = fav[0].listing
						# Make a request
						req = Request.objects.create(
							listing = listing,
							offer_price = offer_price,
							buyer = user,
							seller = listing.seller,
							accepted = False
						)
						print req
						seller = listing.seller.first_name if listing.seller.first_name else 'the seller'
						msg = "We'll let " + seller + " know and you'll hear back soon."
						# Remove saved favorite
						fav.delete()
						# Offer notification
						book = listing.book
						to_email = [listing.seller.email]
						subject = 'You have an offer for %s on TigerTales'  % (book.title)
						from_email = settings.DEFAULT_FROM_EMAIL
						message = "Hello, a potential buyer has sent you an offer for on one of your listings. Please visit our website for next steps."
						html_template = loader.render_to_string(
						          settings.BASE_DIR + '/app/templates/app/emails/request_from_seller',
						          {
						              'book_title': book.title,
								      'buyer_name': user.first_name,
									  'book_offer': offer_price,
									  'book_price': listing.price,
									  'book_image': book.imageURL,
								  }
						)
						send_mail(
							subject,
						    message,
						    from_email,
						    to_email,
						    fail_silently=False,
						  	html_message = html_template,
						)
					else:
						err_msg = 'Sorry, this listing was just taken off the market!'
					show_modal = 'true'
				# Delete the item from the user's favorites
				if 'delete-'+str(i) in request.POST:
					print 'deleting a favorite'
					fav = Cart.objects.filter(id=fav_id)
					if fav.exists():
						fav.delete()
					msg = "We've removed the listing from your favorites."
					show_modal = 'true'

	# If there is a numeric arg, remove entry with corresponding id do something
	favorites = Cart.objects.filter(user = user)
	RequestFormset = formset_factory(NewRequestForm, extra = len(favorites))
	init_list = []
	for i in range(len(favorites)):
		init_list.append({'fav_id': favorites[i].id})
	formset = RequestFormset(initial = init_list)

	print 'user', user
	print 'favorites', favorites

	# If there is a numeric arg..
	if id>0:
		# Procecss request to delete request
		try:
			r = Request.objects.get(id=id)
			print r
			r.delete()
			err_msg = 'Ok, we\'ve deleted your request.'
			show_modal = 'true'
		except: # Avoid crashing on relaod after already deleting an item
			HttpResponseRedirect(reverse('app:cart'))
	# Get pending requests for buyer
	pending = Request.objects.filter(buyer=user)
	context = {
		'net_id': user.net_id,
		'favorites': favorites,
		'first_name': user.first_name,
		'last_name': user.last_name,
		'formset': formset,
		'msg': msg,
		'err_msg': err_msg,
		'show_modal': show_modal, # Note: this must be 'true' or 'false'
		'requests': pending
	}
	return render(request, 'app/cart', context)

@login_required
def store(request,id=-1):
	user = request.user.user
	show_modal = 'false'
	err_msg = ''
	msg = ''
	matches = []
	modal_form = ''
	new_listing_book_name = ''
	condition = ''
	emails = []
	match = None
	if request.method == 'POST':
		form = ListingForm(request.POST)
		# Standard request to process form
		if form.is_valid():
			clean = form.cleaned_data
			book_title = clean.get('book')
			seller_price = clean.get('price')
			condition = clean.get('condition')
		else:
			book_title = "THIS WONT MATCH ANYTHING"
		# Match request to choose one title amongst many
		if 'match' in request.POST:
			matches = Book.objects.filter(title__iexact = request.POST['match'])
			seller_price = request.POST['price']
			condition = request.POST['condition']
			match = matches[0]
		else:
			matches = Book.objects.filter(title__icontains=book_title)
			if len(matches) == 1:
				match = matches[0]
		# Process new listing
		if match and seller_price:
			today = datetime.today()
			print 'you are here'
			print 'condition is', condition
			listing = Listing.objects.create(
				date_created = today,
				date_updated = today,
				book = match,
				seller = user,
				condition = condition,
				price = seller_price
			)
			print listing
			new_book = matches[0].title if matches[0].title else 'the book'
			msg = 'We\'ll add ' + new_book + ' to the exchange and maybe a tiger will bite.'
			# New Listing Notification
			book = matches[0]
			notify = list(Notifications.objects.filter(book_name=book.id))
			for entry in notify:
				emails.append(User.objects.get(user_id = entry.user_id).email)
			print emails
			subject = '%s is available on TigerTales'  % (book.title)
			from_email = settings.DEFAULT_FROM_EMAIL
			message = "Hello, %s was just added to TigerTales. Please visit our website to submit an offer for it." % (book.title)
			html_template = loader.render_to_string(
			          settings.BASE_DIR + '/app/templates/app/emails/new_book_email',
			          {
			              'book_title': book.title,
						  'book_price': listing.price,
						  'book_image': book.imageURL,
					  }
			)
			send_mail(
				subject,
			    message,
			    from_email,
			    emails,
			    fail_silently=False,
			  	html_message = html_template,
			)
		# Too many matches
		if not match and len(matches) > 1:
			err_msg = 'The title matches multiple books. Which of the following did you mean?'
			print 'now you are here'
			print 'and now condition is', condition
			modal_form = ListingForm(initial={'price': seller_price, 'condition': condition})
			modal_form.fields['price'].widget = forms.HiddenInput()
			modal_form.fields['book'].widget = forms.HiddenInput()
			modal_form.fields['condition'].widget = forms.HiddenInput()
		# No matches
		if not match and len(matches) < 1:
			err_msg = 'Sorry, the title didn\'t match any current course books.'
		show_modal = 'true'
	# If there is a numeric arg...
	if id>0:
		# Process to accept request and notify both parties
		if 'accept' in request.path_info:
			print 'accept'
			try:
				# Change the request status to accepted!
				r = Request.objects.get(id=id)
				print r
				r.accepted = True;
				r.save()
				# Remove all other requests assosciated with this listing!
				r_listing = r.listing
				Request.objects.filter(listing=r_listing).delete()
				# Take listing off the market too!
				r_listing.delete()
				bidder = r.buyer.first_name if r.buyer.first_name else 'the bidder'
				msg = 'We\'ve accepted the request and will connect you to ' + bidder + '.'
				# Introduction email
				book = r.listing.book
				to_email = [r.buyer.email, r.seller.email]
				subject = 'Your TigerTales Transaction for %s has been Accepted' % (book.title)
				from_email = settings.DEFAULT_FROM_EMAIL
				message = "Hello, your pending transaction in TigerTales has been accepted. Please visit our website for next steps."
				html_template = loader.render_to_string(
				          settings.BASE_DIR + '/app/templates/app/emails/intro_email',
				          {
				              'book_title': book.title,
						      'buyer_first_name': r.buyer.first_name,
							  'buyer_last_name': r.buyer.last_name,
							  'seller_first_name': r.seller.first_name,
							  'seller_last_name': r.seller.last_name,
							  'seller_facebook': r.seller.facebook,
							  'seller_venmo': r.seller.venmo_handle,
							  'buyer_facebook': r.buyer.facebook,
							  'buyer_venmo': r.buyer.venmo_handle,
							  'agreed_price': r.offer_price,
							  'book_image': book.imageURL,
						  }
				)
				send_mail(
					subject,
				    message,
				    from_email,
				    to_email,
				    fail_silently=False,
				  	html_message = html_template,
				  )
			except:
				err_msg = 'Sorry, this request was removed.'
			show_modal = 'true'
		# Process to deny request and notify buyer
		elif 'decline' in request.path_info:
			print 'decline'
			try:
				r = Request.objects.get(id=id)
				r.delete()
				bidder = r.buyer.first_name if r.buyer.first_name else 'the bidder'
				msg = 'Ok, we\'ll let ' + bidder + ' know.'
				# Notification to tell buyer of rejection
				book = r.listing.book
				to_email = [r.buyer.email]
				subject = 'Your TigerTales Offer for %s was Denied' % (book.title)
				from_email = settings.DEFAULT_FROM_EMAIL
				message = "Hello, we are regretful to inform you your offer was denied. If you would like to submit another offer, please visit our website."
				html_template = loader.render_to_string(
						  settings.BASE_DIR + '/app/templates/app/emails/request_denied',
						  {
							  'book_title': book.title,
							  'buyer_name': r.buyer.first_name,
							  'book_offer': r.offer_price,
							  'book_price': r.listing.price,
							  'book_image': book.imageURL,
						  }
				)
				send_mail(
					subject,
					message,
					from_email,
					to_email,
					fail_silently=False,
					html_message = html_template,
				  )
			except:
				pass
			show_modal = 'true'
		# Process to delete listing
		else:
			try:
				listing = Listing.objects.get(id=id)
				print listing
				listing.delete()
				err_msg = "OK! We've deleted the listing."
				show_modal = 'true'
			except: # Avoid crashing on reload after already deleting an item
				HttpResponseRedirect(reverse('app:store'))

	pending = Request.objects.filter(seller=user, accepted=False)
	active = Listing.objects.filter(seller=user)
	print active
	form = ListingForm()
	context = {
		'net_id': user.net_id,
		'active_listings': Listing.objects.filter(seller=user),
		'first_name': user.first_name,
		'last_name': user.last_name,
		'form': form,
		'msg': msg,
		'err_msg': err_msg,
		'matches': matches,
		'modal_form': modal_form,
		'requests': pending,
		'show_modal': show_modal # Note: this must be 'true' or 'false'
	}
	return render(request, 'app/store', context)

@login_required
def profile(request,id=-1):
	user = request.user.user
	courselist = []
	search_query = []
	books = []
	booklist = []
	all_courses = []
	err_msg = ''
	show_modal = 'false'

	threshold = timedelta(days = 0, minutes = 0, seconds = 10)
	if (timezone.now() - request.user.date_joined) < threshold:
		print ("first login")
		show_modal = 'true'
		err_msg = 'Welcome! Since this is your first time logging in, please fill out some information to start using the exchange. Happy textbook hunting!'

	# Form handling
	if request.method == 'POST':
		form = ProfileForm(request.POST)
		if form.is_valid():
			clean = form.cleaned_data
			first_name = clean.get('first_name')
			last_name = clean.get('last_name')
			venmo = clean.get('venmo')
			facebook = clean.get('facebook')
			email = clean.get('email')
			courses = clean.get('courses')
			if first_name:
				user.first_name = first_name
			if last_name:
				user.last_name = last_name
			if venmo:
				user.venmo_handle = venmo
			if facebook:
				user.facebook = facebook
			if email:
				user.email = email
			user.notify_email = True
			user.save()
			if courses:
				search_query = courses
				# Collects and Returns Course object
				course = Course.objects.filter(course_name__icontains=search_query.strip())
				if course.exists():
					course = course[0]
					# Avoid letting the user re-add the course!
					if not CourseList.objects.filter(user=user, course=course):
						courselist = CourseList(
							user = user,
							course = course
						)
						courselist.save()
						print courselist
						print "saving course here"
					else:
						err_msg = 'You\'ve already added this course!'
						show_modal = 'true'
				else:
					err_msg = "Sorry, we couldn't add the course. Please follow the example the format."
					show_modal = 'true'

	# If there is a numeric arg, remove course from the user's courselist
	if id>0:
		# Add or remove notification for the appropriate book
		if 'notify' in request.path_info:
			notification = Notifications.objects.filter(book_name = id, user_id = user.id)
			if notification.exists():
				notification.delete()
			else:
				courseID = Book.objects.filter(id=id)[0].course_id
				req = Notifications.objects.create(
							book_name = id,
							user_id = user.id,
							course_id = courseID
						)
		# Add or remove course from the user's list of courses
		else:
			course = Course.objects.filter(id=id)
			# Check that course exists
			if course.exists():
				course = course[0]
				cl_entry = CourseList.objects.filter(user=user, course=course)
				booksToDelete = Notifications.objects.filter(course_id = id)
				for deleteBook in booksToDelete:
					deleteBook.delete()
				# Check that course is in user's course list
				if cl_entry.exists():
					cl_entry.delete()

	# Get course list
	all_courses = CourseList.objects.filter(user=user)
	if len(all_courses) > 0:
		print 'User\'s courses'
		for i in range (0, len(all_courses)):
			print all_courses[i]
			books = Book.objects.filter(course=all_courses[i].course)
			booklist.append(books)

	notifyList = []

	for books in booklist:
		for book in books:
			notify = Notifications.objects.filter(user_id=user.id, book_name=book.id).exists()

			if notify:
				notifyList.append(1)
			else:
				notifyList.append(0)

	course_ids = []
	for courseClass in all_courses:
		course_ids.append(courseClass.course_id)

	# Reload with blank form (include most recent information)
	form = ProfileForm()
	form.fields['first_name'].widget.attrs.update({"placeholder": user.first_name})
	form.fields['last_name'].widget.attrs.update({"placeholder": user.last_name})
	form.fields['venmo'].widget.attrs.update({"placeholder": user.venmo_handle})
	form.fields['facebook'].widget.attrs.update({"placeholder": user.facebook})
	form.fields['email'].widget.attrs.update({"placeholder": user.email})
	form.fields['courses'].widget.attrs.update({"placeholder": 'e.g. COS333'})

	context = {
		'first_name': user.first_name,
		'last_name': user.last_name,
		'user_id': user.id,
		'net_id': user.net_id,
		'form': form,
		'course_ids': course_ids,
		'notifyList': notifyList,
		'courselist': courselist,
		'all_courses': all_courses,
		'booklist': list(booklist),
		'err_msg': err_msg,
		'show_modal': show_modal # Note: this must be true or false
	}
	return render(request, 'app/profile', context)

@login_required
def about(request, id=-1):
	user = request.user.user
	context = {
	        'first_name': user.first_name,
	        'last_name': user.last_name,
	        'net_id': user.net_id
	    }
	return render(request, 'app/about', context)
