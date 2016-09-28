from django.conf.urls import url

from .views import index, addTodo, completeTodo

app_name = 'dashboard'

urlpatterns = [
    # render view
    url(r'^$', index, name='index'),
    # add a task
    url(r'^addTodo', addTodo, name='addTodo'),
    # perform task
    url(r'^completeTodo', completeTodo, name='completeTodo'),
]
