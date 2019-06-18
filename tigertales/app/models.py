# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


class User(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	net_id = models.CharField(max_length=100)
	first_name = models.CharField(max_length=100, default='')
	last_name = models.CharField(max_length=100, default='')
	venmo_handle = models.CharField(max_length=100, default='')
	facebook = models.CharField(max_length=100, default='')
	email = models.CharField(max_length=250, default='')
	notify_email = models.BooleanField(default=False)
	def __str__(self):
		return self.first_name + " " + self.last_name + " @" + self.net_id

class Course(models.Model):
	course_name = models.TextField()
	course_id = models.TextField()
	def __str__(self):
		return self.course_name

class Notifications(models.Model):
	book_name = models.TextField()
	user_id = models.TextField()
	course_id = models.TextField()
	def __str__(self):
		return self.course_name

class Book(models.Model):
	title = models.TextField()
	amazon_price = models.TextField()
	lab_price = models.TextField()
	puid = models.TextField()
	description = models.TextField()
	imageURL = models.TextField()
	isbn = models.TextField()
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	def __str__(self):
		return self.title

class CourseList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    def __str__(self):
	       return self.course.course_name

class Listing(models.Model):
	date_created = models.DateTimeField('date created')
	date_updated = models.DateTimeField('date updated')
	book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
	seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	condition = models.TextField()
	price = models.TextField()
	def __str__(self):
		return self.book.title+", "+self.seller.net_id+" is selling for "+str(self.price)+"\ncondition: "+self.condition

# Note: this acts more like a "favorites" - have to collect all listings in cart
# where user == id to get the cart for a specific user
class Cart(models.Model):
	listing = models.ForeignKey(Listing)
	user = models.ForeignKey(User)
	currentOffer = models.TextField()
	def __str__(self):
		return self.listing.book.title + " saved by " + self.user.net_id

class Request(models.Model):
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
	offer_price = models.CharField(max_length=100, default='')
	buyer = models.ForeignKey(User, related_name='buyer')
	seller = models.ForeignKey(User, related_name='seller')
	accepted = models.BooleanField(default=False)
	def __str__(self):
		return self.seller.net_id + " offering " + self.offer_price + " for " + self.listing.book.title

@receiver(user_logged_in)
def setUserProfile(sender, request, user, **kwargs):
	print 'logged in', user.username
	print 'last login', user.last_login
	print 'date created', user.date_joined
	# Create user, shop, and cart for authenticated user
	(obj, user_created) = User.objects.get_or_create(user=user)
	if user_created:
		print "Creating profile"
		net_id = obj.user.username
		# Initialize net_id
		obj.net_id = net_id
		obj.save()
