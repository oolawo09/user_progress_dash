from django.conf.urls import url

from .todo_controllers import addTodo, do
from .controllers import indexController

app_name = 'dashboard'

urlpatterns = [
    # render view
    url(r'^$', indexController, name='index'),
    # add a task
    url(r'^addTodo', addTodo, name='addTodo'),
    # perform task
    url(r'^do', do, name='do'),
]
