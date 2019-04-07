from django.conf.urls import url

import contact
from contact import views
urlpatterns = [
    url(r'^$',contact.views.contact,name='contactus'),
]