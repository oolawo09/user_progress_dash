from django.conf.urls import url

from . import views

app_name = 'dashboard'

urlpatterns = [
    url(r'^add_todo' ,views.add_todo, name='add_todo'),
    url(r'^$', views.index, name='index'),

]
