from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'app'

urlpatterns = [
	url(r'^$', views.index, name='landing'),
	url(r'^login/$', views.login, name='cas_ng_login'),
	url(r'^logout/$', views.logout, name='cas_ng_logout'),
	url(r'^main/$', views.main, name='main'),
	url(r'^main/([0-9]+)/$', views.main, name='main'),
	url(r'^cart/$', views.cart, name='cart'),
	url(r'^cart/([0-9]+)$', views.cart, name='cart'),
	url(r'^store/$', views.store, name='store'),
	url(r'^store/([0-9]+)/$', views.store, name='store'),
	url(r'^store/decline/([0-9]+)/$', views.store, name='store'),
	url(r'^store/accept/([0-9]+)/$', views.store, name='store'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^profile/([0-9]+)$', views.profile, name='profile'),
	url(r'^profile/notify/([0-9]+)/$', views.profile, name='profile'),
	url(r'^about/$', views.about, name='about'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
