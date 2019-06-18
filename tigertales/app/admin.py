# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Cart, Course, User, Book, Listing, Request

admin.site.register(Cart)
admin.site.register(Course)
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Listing)
admin.site.register(Request)
