from django.conf.urls import url

from .todo_controllers import addTodo
from .controllers import indexController

app_name = 'dashboard'

urlpatterns = [
    # add a todo
    url(r'^addTodo', addTodo, name='addTodo'),
    # render the view
    url(r'^$', indexController, name='index'),
]
