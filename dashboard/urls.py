from django.conf.urls import url

from . import views, controllers

app_name = 'dashboard'

urlpatterns = [
    #add a todo
    url(r'^addTodo' ,controllers.addTodo, name='addTodo'),
    #render the view
    url(r'^$', views.index, name='index'),
]
