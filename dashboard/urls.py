from django.conf.urls import url

from . import views

app_name = 'dashboard'

urlpatterns = [
    url(r'^addTodo' ,views.addTodo, name='addTodo'), 
    url(r'^todo', views.todo, name='todo'), 
]
