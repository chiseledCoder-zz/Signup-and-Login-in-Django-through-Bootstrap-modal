from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^user/login$', views.user_login, name='user_login'),
	url(r'^user/signup$', views.user_signup, name='user_signup'),		
]