"""tigertales URL Configuration"""

from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
	url(r'^', include('app.urls')), # Made app/ urls the default
    url(r'^admin/', admin.site.urls)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
